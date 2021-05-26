"""
eval_silsil
-------

Script to evaluate the results(bsigs) of a SilSil test

:org:           Continental AG
:author:         Hirivate Somashekar, Sagar02

:version:       $Revision: 1.6 $
:contact:       $Author: Hirivate Somashekar, Sagar02 (uids3923) (uids3923) $ (last change)
:date:          $Date: 2020/11/06 08:38:21CET $
"""

MEMBER_VERSION = "$Revision: 1.6 $"
print __file__ + " " + MEMBER_VERSION

import os
import re
import numpy
import sys
import shutil
import json
import logging
from datetime import datetime
import xml.dom.minidom
sys.path.append(r"externals")

from externals.junit_xml import TestSuite, TestCase, decode
from collections import namedtuple
from collections import defaultdict
from collections import OrderedDict
from operator import attrgetter
import xml.etree.ElementTree as ElementTree
from externals.stk.io.signalreader import SignalReader

from six import iteritems

SignalResult = namedtuple("SignalResult", "result, len_diff, diff")


class FilterParseError(Exception):
    pass


class ComparisonError(Exception):
    pass


class SilSilResults(object):
    """
    Container class for Sil Sil results
    """
    def __init__(self, recording_name, signal_diffs):
        """

        :param recording_name: file_path of the recording used for simulating
        :type recording_name: str
        :param signal_diffs:
        :type signal_diffs: SilSilDifferences
        :return:
        """
        #: filename of the recording. extracted from given path :type: str
        self._recording_name = os.path.basename(recording_name)
        #: overall result of the sil_sil_comparison :type: bool
        self._result = signal_diffs.result
        #: detailed results of the sil_sil_comparison :type: SilSilDifferences
        self._signal_diffs = signal_diffs
        pattern = re.compile(".*_sil_sil([\w\d\._]+).bsig")
        #: name of the result. name is combining recording name and result suffixes :type: str
        try:
            self._name = self._recording_name + "".join(sorted([(pattern.match(signal_diffs.file1).group(1)),
                                                                (pattern.match(signal_diffs.file2).group(1))]))
        except AttributeError:
            self._name = self._recording_name

    @property
    def recording(self):
        return self._recording_name

    @property
    def name(self):
        return self._name

    def already_compared(self, file1, file2):
        """
        checks if this combination files was already compared
        :param file1: name\path of reference file
        :type file1: str
        :param file2: name\path of file to be checked against
        :type file2: str
        :return: returns true if this combination was already compared, else false
        :rtype: bool
        """
        return (file1 == self._signal_diffs.file1 or file1 == self._signal_diffs.file2) and\
               (file2 == self._signal_diffs.file1 or self._signal_diffs.file2)

    @property
    def struct_differences(self):
        return self._signal_diffs.struct_differences

    @property
    def components(self):
        return self._signal_diffs.components

    def sample_time(self, sample):
        return self._signal_diffs.sample_time(sample)


class SilSilDifferencesBsig(object):
    """
    Class for computing differences of 2 bsig files.
    Therefor every signal in this file is diffed (if not added to the black list).
    Signal url: SIM VFB.COMPONENT.STRUCTURE.SUBSTRUCTURE0....SUBSTRUCTUREn.Signal
    After diffing the signals the diffs are merged to the structures of the component and to the components itself.
    The result is true if all signals are equal otherwise it is False.
    """
    mts_time_stamp_url = "MTS.Package.TimeStamp"

    def __init__(self, bsig1, bsig2, black_list, white_list, exported_signals=None):
        """
        checks if this combination files was already compared
        :param bsig1: name\path of the reference bsig file
        :type bsig1: str
        :param bsig2: name\path of the bsig file to be checked against
        :type bsig2: str
        :param black_list: list of signals that should be ignored for the comparison
        :type black_list: list[str]
        :param white_list: list of signals that should be used for the comparison
        :type white_list: list[str]
        """

        self._diffs = {}
        self._structures = {}
        self._components = {}
        self._result = True

        with SignalReader(bsig1) as sr1, SignalReader(bsig2) as sr2:
            if len(sr1[SilSilDifferencesBsig.mts_time_stamp_url]) != len(sr2[SilSilDifferencesBsig.mts_time_stamp_url]):
                #check if the number of samples match in both files. If not raise an exception
                raise ComparisonError("Compared files have different number of samples! Files: %s, %s" % (bsig1, bsig2))

            #: gets the list of mts timestamps (in us) :type: numpy.array
            mts_time_stamps = sr1[SilSilDifferencesBsig.mts_time_stamp_url]

            first_diff_min = len(mts_time_stamps)
            min_signals = []
            dif_signals_dict = OrderedDict()

            try:
                #: provides a list of times in micro seconds. Each entry corresponds to one sample in the data :type: list
                self._sample_times = (mts_time_stamps - mts_time_stamps[0])

                # compare every signal available in the signal reader or if the white_list is available
                #  every signal in the white_list
                sr1_signals = sr1.signal_names
                sr1_split = [signal.split(".") for signal in sr1_signals]
                sr2_split = [signal.split(".") for signal in sr2.signal_names]
                signal_list = [get_related_signal(sig, sr1_split) for sig in white_list] if white_list else sr1_signals
                sr2_signals = [get_related_signal(sig, sr2_split) for sig in signal_list]
                sr1_signals_filtered = []
                sr2_signals_filtered = []
                for signal, signal_ref in zip(signal_list, sr2_signals):
                    # check if signal is not in the black list
                    if not (signal in black_list or signal_ref in black_list):
                        sr1_signals_filtered.append(signal)
                        sr2_signals_filtered.append(signal_ref)

                sr1_data_list = sr1[sr1_signals_filtered]
                sr2_data_list = sr2[sr2_signals_filtered]
                print "Extracted Data"
                for signal, sr1_data, sr2_data in zip(signal_list, sr1_data_list, sr2_data_list):
                    # Nasty workaround
                    if signal == 'Algo.CP_Version':
                        continue
                    split_signal = signal.split(".")
                    struct = split_signal[1] + "." + split_signal[2]  # 1: Component 2: Structure (at least for cam)

                    # in case the simcon file was handed to the evaluation (self._test_cases != None) the signal
                    # names should be updated to the test_case ones (PPortNames)
                    if exported_signals:
                        for test_case_name, test_case_value in exported_signals.iteritems():
                            if any(name.startswith(struct) for name in test_case_value["meas_freezes"]):
                                struct = test_case_name
                                break

                    diff = (sr1_data - sr2_data).astype(bool)
                    self._diffs[signal] = diff
                    # in case of arrays merge them
                    try:
                        temp_diff = numpy.zeros(diff.shape[0])
                        for i in range(diff.shape[1]):
                            temp_diff = numpy.logical_or(temp_diff, diff[:, i])
                        diff = temp_diff
                    except IndexError:
                        pass
                    if numpy.count_nonzero(diff):
                        first_diff = numpy.nonzero(diff)[0][0]
                        overall_diff = numpy.nonzero(diff)[:][:]
                        dif_signals_dict.update({signal: overall_diff})
                        if first_diff < first_diff_min:
                            first_diff_min = first_diff
                            min_signals = [signal]
                        if first_diff == first_diff_min:
                            min_signals.append(signal)
                    self._structures[struct] = numpy.logical_or(diff, self._structures.setdefault(struct, diff))

                # get component overview => merged from structures
                for structure in self._structures:
                    diff = self._structures[structure]
                    number_of_diffs = numpy.count_nonzero(diff)
                    self._result = self._result and number_of_diffs == 0
                    self._structures[structure] = SignalResult(number_of_diffs == 0, number_of_diffs, diff)
                    component = structure.split(".")[0]
                    self._components[component] = numpy.logical_or(diff, self._components.setdefault(component, diff))

                if min_signals:
                    print"\n First difference occured after %f micro seconds at index %d. Signals showing differences " \
                         "at that moment:" %(self._sample_times[first_diff_min] , first_diff_min)
                    for signal in min_signals:
                        print signal
                        logging.debug("First deviation in %s at %f micro seconds"\
                                      % (signal, self._sample_times[first_diff_min]))

                if dif_signals_dict:
                    print ("\nSignals showing differences at that moment are:")
                    for k, v in dif_signals_dict.items():
                        print ('\"{}\" has its difference at index {}'.format(k, v))
                        logging.debug('\"{}\" has its difference at index {}'.format(k, v))
            except (KeyError, IndexError):
                self._sample_times = None
                raise ComparisonError("Files have 0 samples.! Files: %s, %s" % (bsig1, bsig2))

        print "Diff Done !"

    def sample_time(self, sample):
        try:
            res = self._sample_times[sample] if self._sample_times is not None else 0
        except IndexError:
            res = self._sample_times[-1]
        return res

    @property
    def differences(self):
        return self._diffs

    @property
    def struct_differences(self):
        return self._structures

    @property
    def components(self):
        return self._components

    @property
    def result(self):
        return self._result


def get_related_signal(signal, signal_list_split):
    """
    finds the related signal to a given signal out of a signal list
    :param str signal: signal to find the related one
    :param list[tuple[str]] signal_list_split: list to find one related item to the given signal
    """
    signal_split = signal.split(".")
    related_signal = []
    matching_distance = 0
    #iterate over the whole list
    for signal_split_reference in signal_list_split:
        distance = 0
        while True:
            distance -= 1
            # check if the signals still have one item left (len < distance) and of the items are equal
            if len(signal_split_reference) < distance * -1 or len(signal_split) < distance * -1 or \
                    signal_split[distance] != signal_split_reference[distance]:
                # items not equal or no items left
                distance += 1
                # check if the distance is equal to the current matching distance => add the signal to the list
                if distance == matching_distance:
                    related_signal.append(".".join(signal_split_reference))
                # check if the distance is smaller than the current matching distance
                if distance < matching_distance:
                    # set new matching distance to the distance
                    matching_distance = distance
                    # create a new list with only one signal (the current one)
                    related_signal = [".".join(signal_split_reference)]
                break

    # check if there is more than one matching signal (should never happen)
    if len(related_signal) > 1:
        print "more than one related signal found for %s. Please check! Matching signals: " % signal
        print related_signal

    # get the first matching signal (normally there should only be one). in case there is no signal returns null
    return related_signal[0] if related_signal else None


class SilSilDifferences(object):
    """

    """

    diff_types = {"bsig": SilSilDifferencesBsig}

    def __init__(self, file1, file2, black_list, white_list=None, exported_signals=None):
        white_list = white_list if white_list else []
        extension = file1.split(".")[-1]
        if extension != file2.split(".")[-1]:
            raise ComparisonError("Different types of files are going to be compared! Files: %s, %s" % (file1, file2))

        try:
            # choose the evaluation_type\diff mechanism according to the file extension
            self._differences = SilSilDifferences.diff_types.get(extension)(file1, file2, black_list, white_list,
                                                                            exported_signals)
        except TypeError:  # raised if the default value None is used. Since None is not callable an TypeError is raised
            print "No evaluation\diff mechanism implemented for sil_sil data_type extension %s" % extension

        self._file1 = file1
        self._file2 = file2

    @property
    def file1(self):
        return self._file1

    @property
    def file2(self):
        return self._file2

    @property
    def result(self):
        return self._differences.result

    @property
    def differences(self):
        return self._differences.differences

    @property
    def struct_differences(self):
        return self._differences.struct_differences

    @property
    def components(self):
        return self._differences.components

    def sample_time(self, sample):
        return self._differences.sample_time(sample)


class SilSilEvaluation(object):

    def __init__(self, bsig_path="", bsigs=None,  logger=None, checkpoint="No checkpoint specified!",
                 test_type="sil_sil"):
        """

        :param bsig_path: path to the bsig folder
        :type bsig_path: str
        :param bsigs: list of bsigs to be compared
        :param str checkpoint: label of the checkpoint the test is conducted with

        :return: self
        """
        self._blacklist = []
        # #:list of signals to be ignored for comparison. Extracted from mts cfg :type: list[str]
        # self._blacklist = self._get_signal_list_from_config_file(filter_path, "SIL-SIL Blacklist")

        #:overall result. True if everything is equal. False if one signal (or more is deviating) :type: bool
        self._result = True

        #:detailed results :type: dict[list[SilSilResults]]
        self._results = {}

        #: test cases extracted from the sim connection file if available :type: list[str]
        self._test_cases = None

        #: dict of exported signals, extracted from exporter setup file of available :type: dict[dict]
        self._exported_signals = None

        #: dict of exporter, extracted from exporter setup file of available :type: dict[dict]
        self._exporter = None

        self._logger = logger

        #: label of the checkpoint the test is conducted with :type: str
        self._checkpoint = checkpoint

        # get all bsig files from the bsig path
        try:
            bsigs = [] if bsigs is None else bsigs
            if bsig_path:
                bsigs.extend([os.path.join(bsig_path, f) for f in os.listdir(bsig_path) if
                              os.path.isfile(os.path.join(bsig_path, f)) and f.endswith("bsig")])
            # prepare dictionary, create empty list per recording
            if test_type == "sil_sil":
                self._bsigs = {os.path.basename(bsig).split("_sil_sil")[0]: [] for bsig in bsigs}
                for bsig in bsigs:
                    # append bsig name to recording list
                    self._bsigs[os.path.basename(bsig).split("_sil_sil")[0]].append(bsig)
            if test_type == "edp_sil":
                self._bsigs = {os.path.basename(bsig).split("_edp_sil")[0]: [] for bsig in bsigs}
                for bsig in bsigs:
                    # append bsig name to recording list
                    self._bsigs[os.path.basename(bsig).split("_edp_sil")[0]].append(bsig)

        except TypeError:
            pass

    def log(self, sev, message):
        try:
            self._logger(sev, message)
        except TypeError:  # self._logger is None
            print sev + ': ' + message

    def compare_bsigs(self):
        """
        Functions compares all available bsigs against each other.
        For this the recording name and the exporter is taken into consideration.
        That means only bsigs from same recording and same exporter are compared.
        :return: None
        :rtype: None
        """
        # remove the exporters rec_file_extension from the recordings name => All results from one recording could be
        # summarized
        compared = False
        for recording, bsigs in self._bsigs.iteritems():
            if self._exporter:
                for exporter in self._exporter.values():
                    if recording.endswith(exporter["rec_file_extension"]):
                        recording = recording.replace(exporter["rec_file_extension"], "")

            # compare all bsigs against each other
            temp_results = []
            for bsig_1 in bsigs:
                for bsig_2 in bsigs:
                    # check if bsig is not the same and check that this combination wasn't already compared
                    if bsig_1 != bsig_2 and not any([res.already_compared(bsig_1, bsig_2) for res in temp_results]):
                        try:
                            self.log("INFO", "Comparing %s and %s" %
                                     (os.path.split(bsig_1)[1], os.path.split(bsig_2)[1]))
                            # set compared to true => at least one recording was compared
                            compared = True
                            # compute diffs
                            signal_differences = SilSilDifferences(bsig_1, bsig_2, self._blacklist, None,
                                                                   None)
                            # add results to result container Todo: check if Results could be merged to Differences
                            result = SilSilResults(recording, signal_differences)
                            # add results to a temp list (Needed for check if comparison was already done)
                            temp_results.append(result)
                            # add result to the class member dict, name is the key
                            self._results.setdefault(result.name, []).append(result)
                            # compute overall result
                            self._result = signal_differences.result and self._result
                        except ComparisonError as e:
                            print e

        if not compared:
            self._result = False
            self.log("ERROR", "No comparison took place! No Results to expect!")

    def write_xml(self, j_unit_path):
        """
        write the results as junit xml
        :param j_unit_path: path to the junit outfile
        :type j_unit_path: str
        :return:
        """

        # overriding TestSuite to add stylesheet support
        class TestSuiteStylesheetSupport(TestSuite):
            @staticmethod
            def to_xml_string(test_suite_list, prettyprint=True, encoding=None, stylesheet=None, properties=None):
                """Returns the string representation of the JUnit XML document.
                @param encoding: The encoding of the input.
                @return: unicode string
                """

                try:
                    iter(test_suites)
                except TypeError:
                    raise Exception('test_suites must be a list of test suites')

                xml_element = ElementTree.Element("testsuites")
                attributes = defaultdict(int)

                # add any properties
                if properties:
                    props_element = ElementTree.SubElement(xml_element, "properties")
                    for k, v in properties.items():
                        attrs = {'name': decode(k, encoding), 'value': decode(v, encoding)}
                        ElementTree.SubElement(props_element, "property", attrs)

                for ts in test_suites:
                    ts_xml = ts.build_xml_doc(encoding=encoding)
                    for key in ['failures', 'errors', 'skipped', 'tests']:
                        attributes[key] += int(ts_xml.get(key, 0))
                    for key in ['time']:
                        attributes[key] += float(ts_xml.get(key, 0))
                    xml_element.append(ts_xml)
                for key, value in iteritems(attributes):
                    xml_element.set(key, str(value))

                xml_string = ElementTree.tostring(xml_element, encoding=encoding)
                # is encoded now
                xml_string = TestSuite._clean_illegal_xml_chars(
                    xml_string.decode(encoding or 'utf-8'))
                # is unicode now

                if prettyprint:
                    # minidom.parseString() works just on correctly encoded binary strings
                    xml_string = xml_string.encode(encoding or 'utf-8')
                    xml_string = xml.dom.minidom.parseString(xml_string)
                    # toprettyxml() produces unicode if no encoding is being passed or binary string with an encoding
                    xml_string = xml_string.toprettyxml(encoding=encoding)
                    if encoding:
                        xml_string = xml_string.decode(encoding)
                    # is unicode now

                if stylesheet:
                    xml_string = xml_string.replace(
                        "<testsuites", "<?xml-stylesheet type='text/xsl' href='%s'?>\n<testsuites" % stylesheet
                    )

                return xml_string

            @staticmethod
            def to_file(file_descriptor, test_suite_list, prettyprint=True, encoding=None, stylesheet=None,
                        properties=None):
                """
                Writes the JUnit XML document to a file.
                """
                xml_string = TestSuiteStylesheetSupport.to_xml_string(
                    test_suite_list, prettyprint=prettyprint, encoding=encoding, stylesheet=stylesheet,
                    properties=properties)
                # has problems with encoded str with non-ASCII (non-default-encoding) characters!
                file_descriptor.write(xml_string)

        # check if j unit path is available. If not available the results are not written
        if j_unit_path:
            test_suites = []

            user = get_user()

            # create a test suite for each tested recording
            for recording_name, results in self._results.iteritems():
                test_suite = TestSuite(name=recording_name)
                test_suites.append(test_suite)

                # if the simcon file was handed to the evaluation (self._test_cases != None) a copy of the test cases
                # is created
                missing_test_cases = list(self._test_cases) if self._test_cases else []

                for res in results:
                    for signal_name in sorted(res.struct_differences):
                        signal_result = res.struct_differences[signal_name]
                        if "Package." not in signal_name:
                            # create test case for each signal available in the results (results already merge the
                            # results of different exporter)
                            test_suite.test_cases.append(self._create_test_case_from_result(signal_name, signal_result))

                            # if exporter setup and simcon file was handed to the evaluation the handled test cases
                            # are identified and and removed from the missing_test_cases list
                            try:
                                missing_test_cases.remove(signal_name)
                            except ValueError:
                                pass

                # create for every test case in missing_test_cases a skipped test case, if there are meas_freezes
                # available for the testcase
                for tc in missing_test_cases:
                    if not "NO_MEAS_FREEZE" in self._exported_signals.get(tc, {"meas_freezes": []})["meas_freezes"]:
                        signal_test_case = TestCase(tc)
                        signal_test_case.add_skipped_info("Testcase skipped")
                        test_suite.test_cases.append(signal_test_case)

                test_suite.test_cases = sorted(test_suite.test_cases, key=attrgetter('name'))

            # write all names in XML-File
            with open(j_unit_path, 'w+') as junit_fd:
                TestSuiteStylesheetSupport.to_file(junit_fd, test_suites, stylesheet="silsil_junit.xslt",
                                                   properties={"Checkpoint": self._checkpoint,
                                                               "Test Result": self.result,
                                                               "Author": user,
                                                               "Date": datetime.now().strftime("%a %d. %B %Y, %H:%M"),
                                                               },
                                                   )

            # copy stylesheet to the folder the junit xml file is written to
            # try:
            #     shutil.copyfile(os.path.join(os.path.split(os.path.abspath(__file__))[0], "silsil_junit.xslt"),
            #                     os.path.join(os.path.split(j_unit_path)[0], "silsil_junit.xslt"))
            #
            # except IOError:
            #     pass

            self.log("Info", "J_Unit_Xml file '%s' written" % j_unit_path)

    def write_component_results(self, out_path):
        """
        write the component results in (so far) a csv file.
        it is exporting the sections of a component where it is showing differences
        :param out_path: path for the outfile
        :type out_path: str
        :return:
        """

        # write those results only if the out path was specified
        if out_path:
            for recording_name, results in self._results.iteritems():
                for res in results:
                    out = ""
                    components = sorted(res.components.keys())
                    # get differing sections for every component
                    for index, component in enumerate(components):
                        component_diff = res.components[component]
                        start = None
                        len_comp_diff = len(component_diff)
                        for i in range(len_comp_diff):
                            #if component_diff[i] == 0 and start is none do nothing
                            #if component_diff[i] == 1 and start not none do nothing
                            if component_diff[i] == 1 and start is None:
                                # diff changes from 0 to 1 => set start to the according sample time
                                start = res.sample_time(i)
                            if component_diff[i] == 0 and start:
                                # diff changes from 1 to 0:
                                # get stop time
                                stop = res.sample_time(i - 1)
                                # write section (start, stop, comp_id) to outfile
                                out += str(start) + ";" + str(stop) + ";" + str(index) + ";" + component + "\n"
                                # reset start
                                start = None
                        if start is not None:
                            out += str(start) + ";" + str(len_comp_diff) + ";" + str(index) + ";" + component + "\n"

                    # write outfile
                    with open(out_path + "\\" + res.name + ".csv", 'w+') as out_file:
                        out_file.write(out)

    def write_angular_gantt_data(self, out_path):
        """

        :param out_path:
        :return:
        """

        # write those results only if the out path was specified
        if out_path:
            for recording_name, results in self._results.iteritems():
                out = []
                components = {}
                struct_diffs = {}
                for res in results:
                    components.update(res.components)
                    struct_diffs.update(res.struct_differences)

                for component in sorted(components.keys()):
                    diff = components[component]
                    if component != "Package":
                        component_tasks = []
                        self._get_tasks(component_tasks, diff, component, res.sample_time, color="#F12232")
                        out.append({"name": component, "tasks": component_tasks})
                        #out.extend({"name": comp, "tasks": components_tasks[comp]} for comp in sorted(components))

                # get differing sections for every component
                for signal_name, signal_result in struct_diffs.iteritems():

                    component = signal_name.split(".")[0]
                    struct_name = signal_name.split(".")[1]
                    if component != "Package":
                        tasks = []
                        struct_row = {"name": struct_name,
                                      "tasks": tasks,
                                      "parent": component,
                                      }
                        self._get_tasks(tasks, signal_result.diff, struct_name, res.sample_time)
                        out.append(struct_row)

                # write outfile
                with open(out_path + "\\" + res.name + ".json", 'w+') as out_file:
                    json.dump(out, out_file)
                with open(out_path + "\\" + res.name + "_pretty.json", 'w+') as out_file:
                    json.dump(out, out_file, indent=4, sort_keys=True)

                self.log("Info", "Gantt results file '%s' written" % (out_path + "\\" + res.name + ".json"))

    @staticmethod
    def _get_tasks(tasks, diff_signal, name, sample_time, color="#F1C232"):
        start = None
        len_comp_diff = len(diff_signal)
        diffs = 0  # used for id. combined with name
        start_second = 0.0
        for i in range(len_comp_diff):
            #if component_diff[i] == 0 and start is none do nothing
            #if component_diff[i] == 1 and start not none do nothing
            if diff_signal[i] == 1 and start is None:
                # diff changes from 0 to 1 => set start to the according sample time
                start = SilSilEvaluation._compute_gantt_time(sample_time(i))
                start_second = sample_time(i)
            if (diff_signal[i] == 0 or i == len_comp_diff - 1) and start:
                # diff changes from 1 to 0:
                # get stop time
                stop = SilSilEvaluation._compute_gantt_time(sample_time(i))
                stop_second = sample_time(i)
                diffs += 1
                # write section (start, stop, comp_id) to outfile
                task = {"id": name + "_" + str(diffs),
                        "color": color,
                        "from": start,
                        "to": stop,
                        "tooltip_string": "%.2f s - %.2f s" % (start_second, stop_second)
                        }
                tasks.append(task)
                # reset start
                start = None

    @staticmethod
    def _compute_gantt_time(sample_time):
        sample_time *= 24
        return int(sample_time), int((sample_time - int(sample_time)) * 60)

    @staticmethod
    def _create_test_case_from_result(signal_name, result):
        """

        :param signal_name:
        :param result:
        :return:
        """

        signal_test_case = TestCase(signal_name)
        if not result.result:
            signal_test_case.add_failure_info("Number of different frame", str(result.len_diff))

        return signal_test_case

    @property
    def result(self):
        return self._result


def get_user():
    if os.getenv("JENKINS_HOME", None):
        return "Jenkins"
    else:
        user_id = os.getenv("USERNAME", "Unknown User")
        return get_name_from_user_id(user_id)


from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4.QtWebKit import *


class Render(QWebPage):

    def __init__(self, url):
        self.app = QApplication(sys.argv)
        QWebPage.__init__(self)
        self.loadFinished.connect(self._load_finished)
        self.mainFrame().load(QUrl(url))
        self.app.exec_()

    def _load_finished(self, result):
        del result
        self.frame = self.mainFrame()
        self.app.quit()


def get_name_from_user_id(user_id):
    page_name = r"https://phonebook.conti.de/apps/cpb/cpb.nsf/main.xsp?q=%s#" % user_id
    name = user_id
    try:
        r = Render(page_name)
        html = str(r.frame.toHtml().toUtf8())
        name = html.split('class="ntHoverName">', 1)[1].split("</a>",  1)[0]
        last_name, first_name = name.split(",", 1)
        first_name = first_name.split("(")[0].strip()
        name = first_name + " " + last_name + " (" + user_id + ")"
    except Exception as e:
        del e
    finally:
        return name


if __name__ == '__main__':

    from argparse import ArgumentParser

    try:

        # parse the arguments
        parser = ArgumentParser(description="Script to evaluate the results of SilSil Test!")

        parser.add_argument("-b", "--bsig_folder", dest="bsig_folder",
                            help="Path to the Bsig folder", metavar="DIR", default=None)
        parser.add_argument("--bsigs", dest="bsigs", default=[], nargs='+', type=str,
                            help="List of bsigs to be compared", metavar="List")
        parser.add_argument("-l", "--cp_label", dest="checkpoint", default="No checkpoint specified!",  nargs='+',
                            help="Label of the checkpoint the test is conducted with", metavar="String")
        parser.add_argument("-o", "--out_path", dest="out_path",
                            help="Output folder for the reports.", metavar="DIR", default=None)
        parser.add_argument("-j", "--junit_path", dest="j_unit_path",
                            help="Defines the output file location for the junit report", metavar="FILE")
        parser.add_argument("-t", "--test_type", dest="test_type", default="sil_sil",
                            help="Type of the test (sil_sil or edp_sil)", metavar="String")

        arguments = parser.parse_args()

        if not arguments.out_path and not arguments.j_unit_path:
            parser.error("The arguments --out_path or --junit_path are mandatory!")

        if not arguments.bsig_folder and not arguments.bsigs:
            parser.error("The arguments --bsig_folder(-b) or --bsigs are mandatory!")

        # For logging Mismatched URLS
        logging.basicConfig(level=logging.DEBUG)
        logger = logging.getLogger()
        handler = logging.FileHandler(arguments.out_path + "\\mismatched_URLs.log", mode='w')
        handler.setLevel(logging.DEBUG)
        logger.addHandler(handler)

        evaluation = SilSilEvaluation(bsig_path=arguments.bsig_folder,
                                      bsigs=arguments.bsigs,
                                      checkpoint=" ".join(arguments.checkpoint),
                                      test_type=arguments.test_type
                                      )

        evaluation.compare_bsigs()
        evaluation.write_xml(arguments.j_unit_path)
        evaluation.write_component_results(arguments.out_path)
        evaluation.write_angular_gantt_data(arguments.out_path)

        sys.exit(0)

    except Exception as exception:
        print exception.message
        sys.exit(-1)
