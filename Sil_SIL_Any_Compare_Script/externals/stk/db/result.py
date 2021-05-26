"""
result.py
---------

test run and results API

:org:           Continental AG
:author:        Sven Mertens

:version:       $Revision: 1.1 $
:contact:       $Author: Mertens, Sven (uidv7805) $ (last change)
:date:          $Date: 2018/06/13 07:57:16CEST $
"""
# pylint: disable=E1101,C0103,R0201,R0924,W0142

__all__ = ["TestSuite", "TestRun", "TestCase", "TestStep"]

# - import Python Modules ----------------------------------------------------------------------------------------------
from os import environ
from cPickle import dumps, loads
from StringIO import StringIO
from gzip import GzipFile
from re import search as research, match
from sympy import Integer, Symbol, sympify, Expr
from sympy.physics import units as su
from numpy import NaN
# from operator import itemgetter

# - local imports -
from stk.db.db_common import BaseDB
from stk.db.table import TableDict, UserTableDict, MeasDict
from stk.util.helper import DefDict

# - defines ------------------------------------------------------------------------------------------------------------
# substitution for units
SSUBS = {Symbol(k): v for k, v in su.__dict__.items()
         if (isinstance(v, Expr) and v.has(su.Unit)) or isinstance(v, Integer)}

# HPC connection IDENT
HPCCONN = "uid=hpc_user;pwd=Baba1234"


# - functions and classes ----------------------------------------------------------------------------------------------
class Result(object):  # pylint: disable=R0902,R0924
    """common test result class
    """
    # type of entry we are
    NONE, RUN, CASE, STEP, EVENT = range(5)
    # type of class
    CLSUB = {}

    # type of mode we do:
    READ, APPEND, WRITE = range(3)

    # assessment states:
    PASSED = 'Passed'
    FAILED = 'Failed'
    NOT_ASSESSED = 'Not Assessed'

    # dict for backward compatibility
    GETATTR = {"exp_result": ("expected",), "meas_result": ("value",), "test_result": ("state",),
               "doorsurl": ("doors", 1), "doorsid": ("doors", 0), "description": ("desc",),
               "collection": ("reccat", 1), "recfile": ("reccat", 3), "recpath": ("reccat", 4),
               "state": ("assessment", 0), "comment": ("assessment", 1), "issue": ("assessment", 2),
               "date": ("assessment", 3), "test_cases": ("__iter__",), "test_steps": ("__iter__",),
               "runtime_details": ("mtsIssues",), "summery_plots": ("image",), "processed_distance": ("driven", 0),
               "processed_time": ("driven", 1), "total_dist": ("driven", 0), "startTS": ("startEnd", 0),
               "endTS": ("startEnd", 1), "total_time": ("driven", 1), "processed_files": ("files",),
               "childs": ("__len__",), "component": ("_component",), "user_account": ("_user", 0),
               "user_name": ("_user", 1), "sim_name": ("_sim_name",), "test_type": ("_ttype",),
               "add_info": ("_add_info",), "id": ("_myId",), "rdid": ("_rdid",), "filter": ("_filter",)}

    def __init__(self, **kwargs):  # pylint: disable=R0912,R0915
        """This is a very complicated class decorated with this beauty -> Abandon all hope, ye who enter here.
        This initializes a new test run, case or step following parameters describe possibles.

        Example of instance:
            parameters described:
                1. string as being the DB connection, can also be a cx_Oracle connection
                2. db prefix to use (for table names)
                3. test run name
                4. test run description
                5. checkpoint
                6. observer name
                7. user, if not you

        with Result("dbq=racadmpe;uid=DEV_MFC4XX_ADMIN;pwd=MFC4XX_ADMIN", "DEV_MFC4XX_ADMIN.", "EMO_TC_004_001",
                    "EMO BBT Test Run", "AL_EMO_01.18.00_INT-1", "EMO_TC_004_001", user='uidv9011', mode=Result.READ)
                                                                                                                as res:

            sub runs or cases are created then via append method, type parameter is needed
            when creating a sub-run (type property returns the type of res (the run):
                rRes = res.append(type=res.type, name="ECU-SIL", desc="sub run 4 testing")

            test cases normally just need a name:
                cRes = rRes.append(name="TC one (1)")

            test steps should have a value in addition and if needed an assessment state (--> GB_ASSESSMENT_STATE):
                cRes.append(name="DISTANCE", desc="first result", value="3*mm", state="passed", measid=50)

        :param connection: (connection string, dbPrefix) or predefined CONN_STRING
        :param name: descriptive name (run, case, step)
        :param desc: description of it (run, case, step)
        :param project: project name (run)
        :param checkpoint: checkpoint string to be set (run)
        :param observer: name of observer doing evaluation (run)
        :param trid: in case you know about, you can use it instead of name, desc, project and checkPoint and observer
        :param collection: collection in use (case, step)
        :param measid: measurement id in use (case, step)
        :param user: NT login of user (run: optional as username can be auto-checked as your name belongs Conti)
        :param value: can be of any type (case, step)
        :param format: additional format for value type if needed (case, step)
        :param unit: can be string or sympy physics unit
        :param expect: expected value will be put into db as string (case, step)
        :param doorsid: the DOORS reference identification (case, step)
        :param doorsurl: the URL to DOORS (case, step)
        """
        # , name, desc, checkpoint, observer, user=environ['username']
        self._type = kwargs.pop('resulttype', Result.NONE)

        self._iterIdx = 0
        self._childs = []
        self._myId = None
        self._attrs = None
        self._restype = "run"
        self._db = kwargs.pop('connection', 'VGA_PWR')

        if type(self._db) in (tuple, list):  # if we should receive (<conn>, <prefix>)
            kwargs['dbPrefix'] = self._db[1]
            self._db = self._db[0]

        self._mode = kwargs.pop('mode', Result.READ)
        self._parent = kwargs.pop('parent', None)
        self._filter = kwargs.pop('filter', ['x.EVENTS', 'x.RESULTS'])
        # self._lock = kwargs.pop('lock', False)
        self._showall = kwargs.pop('showall', False)
        self._collection = 5 * [None]
        coll = kwargs.pop('collection', None)
        if type(coll) == int:
            self._collection[0] = coll
        elif type(coll) == str:
            self._collection[1] = coll
        self._driven = [0] * 2
        self._rdid = 'NULL'
        self._prj = kwargs.pop('project', None)
        self._asId = None
        self._state = self._comment = self._issue = self._asmdt = None
        self._doorsid, self._doorsurl = None, None
        self._value, self._expected = None, None
        self._ttype = None
        self._add_info = None  # unused by now

        if self._type == Result.NONE:  # we're the first / initial one
            if 'trid' not in kwargs:
                self._name = kwargs['name']
                self._desc = kwargs.pop('desc', None)
                self._checkPoint = kwargs['checkpoint']
                self._observer = [kwargs['observer'], None]
            self._user = kwargs.pop('user', [None, None])
            try:
                if type(self._db) == str:
                    self._db = BaseDB(self._db, kwargs.pop('dbPrefix', ""))
                    # do we need that one?, as inserts don't seem to follow this...
                    if self._db.db_type[0] == -1:
                        self._db.execute("ALTER SESSION SET NLS_DATE_FORMAT = 'YYYY-MM-DD HH24:MI:SS'")
                        self._db.execute("ALTER SESSION SET NLS_COMP=LINGUISTIC")
                        self._db.execute("ALTER SESSION SET NLS_SORT=BINARY_CI")
                        self._db.execute("ALTER SESSION SET TIME_ZONE = 'utc'")
                self._db.auto_commit = False
            except Exception as ex:
                raise Exception("DB connection failed!")

            # so, we're the run, let's see if we are in DB
            self._type = Result.RUN
            self._get_project()

            if self._collection[0] is None and self._collection[1] is not None:
                self._collection[0] = self._db.execute("SELECT COLLID FROM CAT_COLLECTIONS WHERE NAME LIKE :name",
                                                       name=self._collection[1])[0][0]

            if 'trid' in kwargs:
                rids = [kwargs['trid']]
                self._name, self._desc, self._prj, self._checkPoint, self._observer[0], self._observer[1], \
                    self._sim_name = \
                    self._db.execute("SELECT r.NAME, r.DESCRIPTION, p.NAME, r.CHECKPOINT, o.NAME, TYPEID, SIM_NAME, "
                                     "FROM VAL_TESTRUN r INNER JOIN GBL_VALOBSERVER o USING(TYPEID) "
                                     "INNER JOIN GBL_PROJECT p USING(PID) WHERE r.TRID = :trid", trid=rids[0])[0]
            else:
                sql = ("SELECT r.TRID FROM VAL_TESTRUN r INNER JOIN GBL_VALOBSERVER o USING(TYPEID) "
                       "INNER JOIN GBL_PROJECT p USING(PID) "
                       "WHERE r.NAME LIKE :name AND r.DESCRIPTION LIKE :descr AND p.NAME LIKE :prj "
                       "AND r.CHECKPOINT LIKE :chkpt AND o.NAME LIKE :obs AND r.IS_DELETED = 0")
                rids = [i[0] for i in self._db.execute(sql, name=self._name, prj=self._prj, chkpt=self._checkPoint,
                                                       descr='%%' if self._desc is None else self._desc,
                                                       obs=str(self._observer[0]))]

            try:
                if len(rids) == 1:  # good!
                    self._myId = rids[0]

                    if self._parent is not None or self._mode == Result.WRITE:  # set older one as deleted
                        # remove also child runs when removing parent
                        self._db.execute("WITH RECUR(TRID, PARENT) AS ("
                                         "SELECT TRID, PARENT FROM VAL_TESTRUN WHERE TRID = :trid "
                                         "UNION ALL"
                                         "SELECT t.TRID, t.PARENT FROM VAL_TESTRUN t INNER JOIN RECUR r "
                                         "ON t.PARENT = r.TRID) "
                                         "UPDATE VAL_TESTRUN SET IS_DELETED = 1 WHERE TRID IN (SELECT TRID FROM RECUR)",
                                         trid=self._myId)

                        self._add_run(False)  # , kwargs.pop("date", None))
                        self._db.commit()
                    elif self._desc is None or self._user[0] is None:
                        self._desc, self._user[0], self._user[1], self._isLocked, self._ttype, self._component, \
                            self._observer[1], self._sim_name = \
                            self._db.execute("SELECT r.DESCRIPTION, LOGINNAME, NVL(u.NAME, ''), IS_LOCKED, "
                                             "NVL(t.NAME, ''), NVL(c.NAME, ''), r.TYPEID, NVL(SIM_NAME, '') "
                                             "FROM VAL_TESTRUN r INNER JOIN GBL_USERS u USING(USERID) "
                                             "LEFT JOIN GBL_TESTTYPE t USING(TTID) "
                                             "LEFT JOIN GBL_COMPONENTS c USING(CMPID) "
                                             "WHERE TRID = :trid", trid=self._myId)[0]
                        self._isLocked = self._isLocked == 1

                elif self._parent is None:  # and add a new entry
                    self._add_run(True)  # , kwargs.pop("date", None))
                    self._db.commit()
            except:
                self._db.rollback()
                raise

        elif self._mode == Result.WRITE:  # parent isn't none, that means we write! (self._parent[0] is not None)
            self._name = kwargs['name']
            try:
                if self._type == Result.RUN:
                    self._desc = kwargs.pop('desc', '')
                    self._observer = kwargs['observer']
                    self._checkPoint = kwargs['checkpoint']
                    self._sim_name = kwargs.pop('sim_name', '')
                    self._get_project()
                    self._add_run(True)  # , kwargs.pop("date", None))
                elif self._db.new_val and self._type == Result.CASE:  # todo: duplicates --> own method
                    self._desc = kwargs['desc']
                    self._doorsid = kwargs['doorsid']
                    if research(r"^(NULL|(?i)([a-z]{2,3}_){1,2}TC(_\d{3}){2}%s)$" %
                                        ("" if self._type == Result.CASE else r"-\d{2}"), self._doorsid) is None:
                        raise ValueError("DOORS ID doesn't match!")
                    self._doorsurl = kwargs['doorsurl']
                    if research(r"^(NULL$|(?i)^doors://[a-z0-9]*:\d*/\?)", self._doorsurl) is None:
                        raise ValueError("DOORS URL doesn't match!")
                    self._expected = kwargs.pop('expected')
                    self._myId = self._db.execute("INSERT INTO VAL_TESTCASE "
                                                  "(TRID, NAME, DESCRIPTION, EXPECTRES, DOORSID, DOORSURL) "
                                                  "VALUES (:pid, :name, :descr, :exp, :did, :dul) RETURNING TCID",
                                                  pid=self._parent.id, name=self._name, descr=self._desc,
                                                  exp=self._expected, did=self._doorsid, dul=self._doorsurl)
                else:
                    self._value = kwargs.pop('value', None)
                    self._unit = kwargs.pop('unit', None)
                    self._desc = kwargs.pop('desc', 'NULL')
                    self._collection[2] = kwargs.pop('measid', None)
                    self._doorsid = kwargs.pop('doorsid', 'NULL').replace('', 'NULL')
                    if research(r"^(NULL|(?i)([a-z]{2,3}_){1,2}TC(_\d{3}){2}%s)$" %
                                ("" if self._type == Result.CASE else r"-\d{2}"), self._doorsid) is None:
                        raise ValueError("DOORS ID doesn't match!")
                    self._doorsurl = kwargs.pop('doorsurl', 'NULL').replace('', 'NULL')
                    if research(r"^(NULL$|(?i)^doors://[a-z0-9]*:\d*/\?)", self._doorsurl) is None:
                        raise ValueError("DOORS URL doesn't match!")
                    self._expected = kwargs.pop('expected', '')

                    if self._collection[2] is not None:
                        self._collection[3], self._collection[4] = \
                            self._db.execute("SELECT RECFILEID, FILEPATH FROM CAT_FILES WHERE MEASID = :meas",
                                             meas=self._collection[2])[0]

                    if self._type in (Result.CASE, Result.STEP):
                        self._restype = kwargs.pop('restype', 'VAL_TEST' +
                                                   ('CASE' if self._type == Result.CASE else 'STEP'))
                        self._rdid = self._add_result(self._value, self._unit, kwargs.pop('format', None),
                                                      kwargs.pop('state', 'Not_Assessed'))
                    else:
                        self._restype = kwargs.pop('restype', 'ValBaseEvent')
                        self._rdid = self._add_event(self._value, self._unit, kwargs['attribs'], kwargs['start_end'],
                                                     kwargs.pop('state', 'Not_Assessed'))
            except:
                self._db.rollback()
                raise
            else:
                self._db.commit()

        else:  # set details (attributes) from run, case, step and event
            self.__dict__.update(kwargs["attribs"])

            if self._type != Result.RUN:
                self._expected = str(self._expected)
                self._comment = str(self._comment)
            try:
                self._oldState, self._oldComment = self._state, self._comment
                self._oldIssue, self._oldAsmdt = self._issue, self._asmdt
            except:
                pass

    def _get_project(self):
        """retrieves the project name"""
        if self._prj is None:
            addon = (" WHERE ROWNUM = 1", "") if self._db.db_type[0] == -1 else ("", " LIMIT 1")
            self._prj = str(self._db.execute("SELECT NAME FROM GBL_PROJECT%s ORDER BY PID ASC%s" % addon)[0][0])

    def _add_run(self, remove):  # , dt) todo: dt is unused
        """adds a run entry"""
        # each run or sub-run contains a name, desc, checkpoint, user, type, when it's started and finished
        self._isLocked = False
        if self._user[0] is None:
            self._user = [environ['username'], '']
        if remove:  # remove older run when totally equal
            self._db.execute("UPDATE VAL_TESTRUN SET IS_DELETED = 1 WHERE NAME LIKE :name AND DESCRIPTION LIKE :descr "
                             "AND PID = (SELECT PID FROM GBL_PROJECT WHERE NAME LIKE :prj) AND CHECKPOINT LIKE :chkpt "
                             "AND TYPEID = (SELECT TYPEID FROM GBL_VALOBSERVER WHERE NAME LIKE :obs)", name=self._name,
                             descr=self._desc, prj=self._prj, chkpt=self._checkPoint, obs=self._observer[0])
        # insert new data as old run probably has childs (cases / events)
        # if dt is None:
        #     dt = self._db.GetCurrDateTime()
        self._observer[1] = self._db.execute("SELECT TYPEID FROM GBL_VALOBSERVER WHERE NAME LIKE :obs",
                                             obs=self._observer[0])[0][0]
        query = ("INSERT INTO VAL_TESTRUN (NAME, DESCRIPTION, PID, STARTTS, ENDTS, CHECKPOINT, USERID, "
                 "TYPEID, PARENT) VALUES (:name, :descr, (SELECT PID FROM GBL_PROJECT WHERE NAME LIKE :prj), "
                 "$DT, $DT, :chkpt, (SELECT USERID FROM GBL_USERS WHERE LOGINNAME LIKE :usr), :obs, :par) "
                 "RETURNING TRID")
        self._myId = self._db.execute(query, name=self._name, descr=self._desc, prj=self._prj, chkpt=self._checkPoint,
                                      usr=self._user[0], obs=self._observer[1],
                                      par=(None if self._parent is None else self._parent.id))

    def _add_result(self, value, unit, frmt, status):  # pylint: disable=R0912,R0915
        """add a result entry for case and step"""

        rdid, value, _ = self._rework_descriptor(self._restype, value, unit)
        self._asId = self._insert_status(status)

        # add result body
        self._myId = self._db.execute("INSERT INTO VAL_RESULT (TRID, RDID, RESASSID, MEASID) "
                                      "VALUES (:pid, :rdid, :asid, :meas) RETURNING RESID",
                                      pid=self._parent.id, rdid=rdid, asid=self._asId,
                                      meas=(None if self._collection[2] is None else self._collection[2]))
        if value is not None:
            self._set_value(value, unit, frmt)

        return rdid

    def _set_value(self, value, unit, frmt):
        """sets / updates the value of a case or step"""

        value, unit = self._rework_value(value, unit)
        self._format = frmt

        if type(value) in (float, int, long):
            self._db.execute("DELETE FROM VAL_RESULTIMAGE WHERE RESID = :resid", resid=self._myId)
            self._db.execute("UPDATE VAL_RESULT SET VALUE=:res WHERE RESID = :resid",
                             res=value, resid=self._myId)

        else:  # other than a simple type...
            if frmt is None:  # use our own format: python objects
                frmt = ""
            value = dumps(value, protocol=2)
            sio = StringIO()
            with GzipFile(mode='wb', fileobj=sio) as gz:
                gz.write(value)
            sio.seek(0)
            value = sio.read()
            sio.close()
            query = ("BEGIN UPDATE VAL_RESULTIMAGE SET FORMAT = :frmt, IMAGE=$LOB WHERE RESID = :res;"
                     "IF SQL%%ROWCOUNT = 0 THEN INSERT INTO VAL_RESULTIMAGE (RESID, FORMAT, IMAGE) "
                     "VALUES (:resid, :frmt, :blob); END IF;END;")
            args = {'frmt': frmt, 'res': self._myId}
            if self._db.db_type[0] == -1:
                binvar = self._db.make_var('blob')
                binvar.setvalue(0, value)
                args['blob'] = binvar
            else:
                args['blob'] = self._db.make_var('blob')(value)
            self._db.execute(query, args)

        self._db.execute("UPDATE VAL_RESULTDESCRIPTOR SET UNITID = :uid WHERE RDID = (SELECT RDID FROM VAL_RESULT "
                         "WHERE RESID = :resid)", uid=unit, resid=self._myId)

    def _add_event(self, value, unit, attrs, startend, status):
        """add a result entry for an event"""

        rdid, value, unit = self._rework_descriptor(self._restype, value, unit)
        self._asId = self._insert_status(status)

        # 1) attrs: [<name>, <desc>, <image>, <title>, <format>, <absts>]
        eaid = self._db.execute("SELECT ATTRTYPEID FROM VAL_EVENTATTRTYPES WHERE NAME LIKE :name AND "
                                "DESCRIPTION LIKE :descr AND UNITID = :unit", name=attrs[1], descr=attrs[2], unit=unit)
        eaid = self._db.execute("INSERT INTO VAL_EVENTATTRTYPES (NAME, DESCRIPTION, UNITID) "
                                "VALUES(:name, :descr, :unit) RETURNING ATTRTYPEID",
                                name=attrs[1], descr=attrs[2], unit=unit) \
            if len(eaid) != 1 else eaid[0][0]

        # 2) image
        binvar = self._db.make_var('blob')
        binvar.setvalue(0, attrs[3])
        eiid = self._db.execute("INSERT INTO VAL_EVENTIMAGE (TITLE, FORMAT, IMAGE) "
                                "VALUES (:title, :frmt, :img) RETURNING ATTRID",
                                title=attrs[4], frmt=attrs[5], bin=binvar)

        # 3) attribute
        eaid = self._db.execute("INSERT INTO VAL_EVENTATTR (EDID, ATTRTYPEID, VALUE) "
                                "VALUES(:edid, :atid, :val) RETURNING ATTRID",
                                edid=eiid, atid=eaid, val=float(value))

        # 4) details
        self._db.execute("INSERT INTO VAL_EVENTDETAILS (SEID, ABSTS) VALUES(:eaid, :det) RETURNING EDID",
                         eaid=eaid, det=attrs[6])

        # 5) startend: [<beginabsts>, <endabsts>, <start_idx>, <stop_idx>]
        self._myId = self._db.execute("INSERT INTO VAL_EVENTS (BEGINABSTS, ENDABSTS, START_IDX, STOP_IDX, MEASID, "
                                      "TRID, RESASSID, RDID, EVENTTYPEID) VALUES(:bats, :eats, :bidx, :eidx, :meas, "
                                      ":trid, :assid, :rdid, :etid, "
                                      "(SELECT EVENTTYPEID FROM VAL_EVENTTYPES WHERE NAME LIKE '%s')) RETURNING SEID",
                                      bats=startend[0], eats=startend[1], bidx=startend[2], eidx=startend[3],
                                      meas=self._collection[2], trid=self._parent.id, assid=self._asId,
                                      rdid=self._rdid, etid=self._restype)
        return rdid

    def _check_gbl_state(self, status):
        """check assessment state on existance, add it on miss, return it's id
        """
        asid = self._db.execute("SELECT ASSSTID FROM GBL_ASSESSMENT_STATE WHERE (VALOBS_TYPEID IS NULL "
                                "OR VALOBS_TYPEID = :oid) "
                                "AND NAME LIKE :name", oid=self._observer[1], name=status)
        return self._db.execute("INSERT INTO GBL_ASSESSMENT_STATE (NAME, VALOBS_TYPEID) VALUES(:name, :oid) "
                                "RETURNING ASSSTID", name=status, oid=self._observer[1]) \
            if len(asid) == 0 else asid[0][0]

    def _insert_status(self, status):
        """insert asmt state for current result
        """
        return self._db.execute("INSERT INTO VAL_ASSESSMENT (USERID, ASSCOMMENT, WFID, ASSDATE, ASSSTID) "
                                "VALUES ((SELECT USERID FROM VAL_TESTRUN WHERE TRID = :trid), 'auto generated', "
                                "(SELECT WFID FROM GBL_WORKFLOW WHERE NAME LIKE 'automatic'), $CD, :assid) "
                                "RETURNING RESASSID", trid=self._parent.id, assid=self._check_gbl_state(status))

    def _rework_value(self, value, unit):
        """rework value/unit as unit is needed for descriptor"""
        if unit is None:
            try:
                if type(value) == str:
                    value = self._pyfy(value)
                value, unit = value.as_two_terms()
                value = int(value) if value.is_number and value.is_integer else float(value)
                unit = str(unit)
            except:
                unit = "None"
        else:
            unit = self._replace_unit(str(unit), False)
        return value, ("(SELECT UNITID FROM GBL_UNITS WHERE LABEL LIKE '%s')" % unit)

    def _rework_descriptor(self, restype, value, unit):
        """reworks the result type: [<name>, <desc>[, <class>]] or just <name>
        """
        value, unit = self._rework_value(value, unit)

        query = r"SELECT RESTYPEID FROM VAL_RESULTTYPES WHERE NAME %s AND DESCRIPTION %s AND CLASSNAME %s"
        if type(restype) == str:
            if self._type == Result.CASE:
                desc = 'Validation TestCase'
            elif self._type == Result.EVENT:
                desc = 'Validation BaseEvent'
            else:
                desc = 'Validation TestStep'
            restype = [restype, desc, 'NULL']
        elif len(restype) < 3:
            restype.append('NULL')
        resid = self._db.execute(query % tuple([('IS NULL' if i == 'NULL' else "LIKE '" + i + "'") for i in restype]))

        if len(resid) == 0:  # add the result type
            resid = self._db.execute("INSERT INTO VAL_RESULTTYPES (NAME, DESCRIPTION, CLASSNAME) "
                                     "VALUES(%s ,%s, %s) RETURNING RESTYPEID" %
                                     tuple([(i if i == 'NULL' else "'" + i + "'") for i in restype]))
        else:
            resid = resid[0][0]

        # add a descriptor
        rdid = self._db.execute("SELECT RDID FROM VAL_RESULTDESCRIPTOR WHERE COLLID = %d AND NAME LIKE '%s' "
                                "AND RESTYPEID = %d AND UNITID = %s AND EXPECTRES LIKE '%s' AND DESCRIPTION %s "
                                "AND REFTAG %s AND DOORS_URL %s AND PARENT %s" %
                                (self._collection[0], self._name, resid, unit, self._expected,
                                 ("IS %s" if self._desc == 'NULL' else "LIKE '%s'") % self._desc,
                                 ("IS %s" if self._doorsid == 'NULL' else "LIKE '%s'") % self._doorsid,
                                 ("IS %s" if self._doorsurl == 'NULL' else "LIKE '%s'") % self._doorsurl,
                                 "IS NULL" if self._parent.rdid is None else ("= %d" % self._parent.rdid)))
        # well, we enter a new one, cos we don't need double
        return (self._db.execute("INSERT INTO VAL_RESULTDESCRIPTOR (COLLID, NAME, RESTYPEID, UNITID, EXPECTRES, "
                                 "DESCRIPTION, REFTAG, DOORS_URL, PARENT) "
                                 "VALUES (%d, '%s', %d, %s, '%s', %s, %s, %s, %s) RETURNING RDID" %
                                 (self._collection[0], self._name, resid, unit, self._expected,
                                  "NULL" if self._desc == 'NULL' else ("'%s'" % self._desc),
                                  "NULL" if self._doorsid == 'NULL' else ("'%s'" % self._doorsid),
                                  "NULL" if self._doorsurl == 'NULL' else ("'%s'" % self._doorsurl),
                                  "NULL" if self._parent.rdid is None else str(self._parent.rdid)))
                if len(rdid) != 1 else rdid[0][0]), value, unit

    def _append(self, **kwargs):
        """append a subitem, e.g. from a run a case or subrun or from a case a step"""
        self._childs = []
        parsed = {i: v for i, v in kwargs.iteritems() if i not in ("connection", "resulttype", "parent",)}

        if self._type == Result.RUN:
            tta = parsed.pop('type', Result.CASE)
            if tta == Result.CASE:
                return TestCase(connection=self._db, resulttype=Result.CASE, parent=self,
                                collection=parsed.pop('collection', self._collection[0]),
                                observer=parsed.pop('observer', self._observer), **parsed)
            elif tta == Result.RUN:  # unpack to make self properties default
                return TestRun(connection=self._db, resulttype=Result.RUN, parent=self,
                               project=parsed.pop('project', self._prj), user=parsed.pop('user', self._user),
                               checkPoint=parsed.pop('checkpoint', self._checkPoint),
                               observer=parsed.pop('observer', self._observer),
                               collection=parsed.pop('collection', self._collection[0]), **parsed)
        elif self._type == Result.CASE:
            if parsed.pop('type', Result.STEP) == Result.STEP:
                return TestStep(connection=self._db, resulttype=Result.STEP, parent=self,
                                collection=parsed.pop('collection', self._collection[0]),
                                measid=parsed.pop('measid', self._collection[2]),
                                observer=parsed.pop('observer', self._observer), **parsed)
            else:
                return TestEvent(connection=self._db, resulttype=Result.EVENT, parent=self,
                                 collection=parsed.pop('collection', self._collection[0]), **parsed)

    def __str__(self):
        """return string text summary of me"""
        if self._type == Result.RUN:
            return "run %s: %s (%s), CP: %s, " \
                   "observer: %s, user: %s" % (str(self._myId), self._name, self._desc, self._checkPoint,
                                               self._observer[0], self._user[0])
        elif self._type == Result.CASE:
            return "case %d: %s (%s)" % (self._myId, self._name, self._desc)
        elif self._type == Result.STEP:
            return ("step %d: %s (%s), value: %s, expected: '%s'"
                    % (self._myId, self._name, self._desc, str(self._value), self._expected))
        elif self._type == Result.EVENT:  # TODO: add more details to string representation
            return "event %d: %s (%s)" % (self._myId, self._name, self._desc)

    def __iter__(self):
        """start iterating through test cases"""
        self._iterIdx = 0
        return self

    def next(self):
        """next child item to catch and return"""
        if self._iterIdx >= len(self):
            raise StopIteration
        else:
            self._iterIdx += 1
            return self[self._iterIdx - 1]

    def sort(self, *args, **kwargs):
        """used by PDF creation, sorting test details"""
        self.get_childs()
        self._childs.sort(*args, **kwargs)

    # def __eq__(self, other):
    #     """equal?"""
    #     return self._myId == other.id
    #
    # def __ne__(self, other):
    #     """not equal?"""
    #     return not self == other
    #
    # def __gt__(self, other):
    #     """greater than?"""
    #     return self._myId > other.id
    #
    # def __lt__(self, other):
    #     """less than?"""
    #     return self._myId < other.id
    #
    # def __ge__(self, other):
    #     """greater or equal?"""
    #     return (self > other) or (self == other)
    #
    # def __le__(self, other):
    #     """greater or equal?"""
    #     return (self < other) or (self == other)

    def __getitem__(self, idx):
        """provide a slice index to be able to iterate through the childs"""
        if type(idx) == int and 0 <= idx < len(self):
            if type(self._childs[idx]) in (tuple, list):
                self.get_childs()
                # self._childs[idx] = Result.CLSUB[self._childs[idx][1]](self._db, name=self._childs[idx][0],
                #                                                        parent=(self._myId, None),
                #                                                        resulttype=self._childs[idx][1],
                #                                                        observer=self._observer, filter=self._filter)
            return self._childs[idx]
        elif (type(idx) == slice and min(0, idx.start, idx.stop) == 0 and
                max(len(self), idx.start, idx.stop) == len(self)):
            if type(self._childs[0] in (tuple, list)):
                self.get_childs()
                # self._childs[i] = Result.CLSUB[self._childs[i][1]](self._db, name=self._childs[i][0],
                #                                                    parent=(self._myId, None),
                #                                                    resulttype=self._childs[i][1],
                #                                                    observer=self._observer, filter=self._filter)
            return self._childs[idx.start:idx.stop]
        else:
            raise IndexError

    def __len__(self):
        """provide length of sub items / childs"""
        if len(self._childs) == 0:
            if self._type in (Result.STEP, Result.EVENT):
                return 0
            elif self._type == Result.RUN:
                self.get_childs()
                return len(self._childs)

            elif self._type == Result.CASE:
                # we're a case and search for steps now...
                sql, sqa = self._get_sql_det(["SEID id, %d type" % Result.EVENT,
                                              "r.RESID id, %d type" % Result.STEP], " UNION ", "")
                self._childs = self._db.execute(sql, **sqa)
                return len(self._childs)

        return len(self._childs)

    def __enter__(self):
        """being able to use with statement
        """
        return self

    def __exit__(self, *_):  # value / traceback
        """close connection"""
        self._close()

    def _close(self, commit=True):
        """commit changes and close connection"""
        if self._type == Result.RUN and self._mode != Result.READ:
            self._db.execute("UPDATE VAL_TESTRUN SET ENDTS = $CT WHERE TRID = :trid", trid=self._myId)
        if commit:
            self._db.commit()
        self._db.close()

    def get_childs(self):
        """retrieve sub items / childs of us
        """
        asmt = "" if self._showall else (" AND (s.VALOBS_TYPEID = %d OR s.VALOBS_TYPEID IS NULL)" % self._observer[1])

        if self._myId is not None:
            sql = [None, None]

            if self._type == Result.RUN:
                # check if we have child runs ...
                self._childs = []
                res = self._db.execute("SELECT r.TRID, r.NAME, r.DESCRIPTION, p.NAME, r.CHECKPOINT, NVL(t.NAME, ''), "
                                       "NVL(c.NAME, ''), NVL(r.SIM_NAME, ''), o.NAME, TYPEID, u.LOGINNAME, NVL(u.NAME, '') "
                                       "FROM VAL_TESTRUN r INNER JOIN GBL_VALOBSERVER o USING(TYPEID) "
                                       "INNER JOIN GBL_USERS u USING(USERID) INNER JOIN GBL_PROJECT p USING(PID) "
                                       "LEFT JOIN GBL_TESTTYPE t USING(TTID) LEFT JOIN GBL_COMPONENTS c USING(CMPID) "
                                       "WHERE r.PARENT = :par AND IS_DELETED = 0 ORDER BY r.NAME", par=self._myId)
                if len(res):
                    runattrs = ["_myId", "_name", "_desc", "_prj", "_checkPoint", "_ttype", "_component", "_sim_name"]
                    attrs, obsv, user = [None] * 8, [None] * 2, [None] * 2
                    attrs[0], attrs[1], attrs[2], attrs[3], attrs[4], attrs[5], attrs[6], attrs[7], obsv[0], obsv[1], \
                        user[0], user[1] = zip(*res)
                    for ridx in xrange(len(attrs[0])):  # ... and load them
                        dict_ = {runattrs[k]: attrs[k][ridx] for k in xrange(len(runattrs))}
                        dict_["_user"] = [user[k][ridx] for k in xrange(len(user))]
                        dict_["_observer"] = [obsv[k][ridx] for k in xrange(len(obsv))]

                        # now add the run
                        self._childs.append(Result.CLSUB[Result.RUN](self._db, parent=self,
                                                                     resulttype=Result.RUN, filter=self._filter,
                                                                     attribs=dict_))  # , lock=self._lock))

                # we can have child cases as well:
                if self._db.new_val:
                    sqi = "SELECT TCID, NAME, DESCRIPTION, EXPECTRES, DOORSID, DOORSURL " \
                          "FROM VAL_TESTCASE WHERE TRID = :trid"
                    caseattrs = ["_myId", "_name", "_desc", "_expected", "_doorsid", "_doorsurl"]
                    attrs = [None] * 6
                    attrs[0], attrs[1], attrs[2], attrs[3], attrs[4], attrs[5] = \
                        zip(*self._db.execute(sqi, trid=self._myId))
                    cls = Result.CLSUB[Result.CASE]

                    for cidx in sorted(set(attrs[0])):
                        dict_ = {caseattrs[k]: attrs[k][cidx] for k in xrange(len(caseattrs))}
                        self._childs.append(cls(connection=self._db, name=cidx, parent=self,
                                                showall=self._showall, resulttype=Result.CASE, filter=self._filter,
                                                attribs=dict_))
                else:
                    sql[1] = ("SELECT r.RESID FROM VAL_RESULT r "
                              "INNER JOIN VAL_RESULTDESCRIPTOR d USING(RDID) "
                              "INNER JOIN VAL_RESULTTYPES y USING(RESTYPEID) "
                              "WHERE r.TRID = :trid AND y.NAME LIKE :name")
                    sqa = {'trid': self._myId, 'name': 'VAL_TESTCASE'}

            elif self._type == Result.CASE:
                # we're a case and search for events / steps now...
                self._childs = []
                sql, sqa = self._get_sql_det(["SEID", "r.RESID"], None, asmt)

            if sql[0] is not None:  # event details
                values = [None] * 2
                attribs = [None] * 4
                evimg = [None] * 3
                evattrs = ["_myId", "_restype", "_name", "_desc", "_state", "_asId", "_comment", "_issue", "_asmdt",
                           "_doorsurl", "_doorsid", "_expected", "_rdid"]
                try:
                    seid, values[0], values[1], attribs[0], attribs[1], attribs[2], attribs[3] = \
                        zip(*self._db.execute("SELECT ed.SEID, ea.VALUE, u.LABEL, ed.ABSTS, et.NAME, et.DESCRIPTION, "
                                              "ea.ATTRID "
                                              "FROM VAL_EVENTDETAILS ed LEFT JOIN VAL_EVENTATTR ea USING(EDID) "
                                              "INNER JOIN VAL_EVENTATTRTYPES et USING(ATTRTYPEID) "
                                              "LEFT JOIN GBL_UNITS u USING(UNITID) WHERE ed.SEID IN (%s) "
                                              "ORDER BY ed.SEID, ea.ATTRID" % sql[0], **sqa))
                    try:
                        sqa['lob'] = 1
                        evimg[0], evimg[1], evimg[2] = \
                            zip(*self._db.execute("SELECT ATTRID, ei.IMAGE, ei.FORMAT "
                                                  "FROM VAL_EVENTDETAILS ed INNER JOIN VAL_EVENTATTR ea USING(EDID) "
                                                  "INNER JOIN VAL_EVENTIMAGE ei USING(ATTRID) "
                                                  "WHERE ed.SEID IN (%s) ORDER BY ed.SEID, ATTRID"
                                                  % sql[0], **sqa))
                    except:
                        evimg = [[], [], []]

                    qry = ("SELECT SEID, rt.NAME, d.NAME, NVL(d.DESCRIPTION, ''), NVL(a.NAME, ''), RESASSID, "
                           "NVL(v.ASSCOMMENT, ''), v.TRACKING_ID, v.ASSDATE, d.DOORS_URL, d.REFTAG, "
                           "NVL(d.EXPECTRES, ''), RDID, COLLID, c.NAME, MEASID, f.RECFILEID, "
                           "f.FILEPATH, e.BEGINABSTS, e.ENDABSTS, e.START_IDX, e.STOP_IDX "
                           "FROM VAL_EVENTS e INNER JOIN VAL_RESULTDESCRIPTOR d USING(RDID) "
                           "INNER JOIN VAL_RESULTTYPES rt USING(RESTYPEID) $SA$ JOIN VAL_ASSESSMENT v USING(RESASSID) "
                           "$SA$ JOIN GBL_ASSESSMENT_STATE a USING(ASSSTID) $SA$ JOIN CAT_COLLECTIONS c USING(COLLID) "
                           "$SA$ JOIN CAT_FILES f USING(MEASID) "
                           "WHERE SEID IN (%s) ORDER BY SEID"
                           % (sql[0])).replace("$SA$", "LEFT" if self._showall else "INNER")
                    sqa.pop('lob')
                    evnts = self._db.execute(qry, **sqa)
                    # , lock=["v.ASSSTID", "v.ASSCOMMENT", "v.TRACKING_ID", "v.ASSDATE"] if self._lock else False
                except:
                    pass
                else:
                    sidx = siidx = vidx = 0
                    for cidx in sorted(set(seid)):
                        # event attribs
                        vidx = next(k for k in xrange(vidx, len(evnts)) if evnts[k][0] == cidx)
                        dict_ = {evattrs[k]: evnts[vidx][k] for k in xrange(len(evattrs))}
                        dict_["_observer"] = self._observer
                        dict_["_collection"] = list(evnts[vidx][len(evattrs):len(evattrs) + 5])
                        dict_["_startEnd"] = list(evnts[vidx][len(evattrs) + 5:len(evattrs) + 5 + 4])

                        # event attrib details
                        vals, attrs, = [], []
                        ssidx = sidx
                        while sidx < len(seid) and seid[sidx] < cidx:  # goto start index
                            sidx += 1
                            ssidx += 1

                        while sidx < len(seid) and seid[sidx] <= cidx:  # loop until
                            # for i in xrange(sidx, eidx):
                            attrs.append((attribs[0][sidx], attribs[1][sidx], attribs[2][sidx],))
                            if values[0][sidx] is None:
                                vals.append(None)
                            elif values[1][sidx] not in (None, 'None', ''):
                                try:
                                    vals.append(self._pyfy(str(values[0][sidx]) +
                                                           ("*" + self._replace_unit(values[1][sidx]))))
                                except:
                                    vals.append(NaN)
                            else:
                                vals.append(values[0][sidx])
                            sidx += 1

                        frmts, imgs = [None] * len(attrs), [None] * len(attrs)

                        while siidx < len(evimg[0]) and evimg[0][siidx] < attribs[3][ssidx]:
                            siidx += 1

                        while siidx < len(evimg[0]) and evimg[0][siidx] <= attribs[3][sidx-1]:
                            for i in xrange(ssidx, sidx):
                                if attribs[3][i] == evimg[0][siidx]:
                                    imgs[i - ssidx] = evimg[1][siidx]
                                    frmts[i - ssidx] = evimg[2][siidx]
                                    break
                            siidx += 1

                        dict_.update({"_attrs": attrs, "_value": vals, "_format": frmts, "_image": imgs})

                        # now add the whole
                        self._childs.append(Result.CLSUB[Result.EVENT](connection=self._db, parent=self,
                                                                       resulttype=Result.EVENT,  # lock=self._lock,
                                                                       filter=self._filter, attribs=dict_))

            if sql[1] is not None:  # case / result details
                # preload results
                # results = ", ".join([str(r[0]) for r in self._childs
                # if type(r) in (tuple, list) and r[1] in (Result.CASE, Result.STEP)])
                #   if len(results):

                sqi = ("SELECT RESID, y.NAME, d.NAME, NVL(d.DESCRIPTION, ''), NVL(a.NAME, ''), RESASSID, "
                       "NVL(v.ASSCOMMENT, ''), v.TRACKING_ID, v.ASSDATE, d.DOORS_URL, d.REFTAG, "
                       "NVL(d.EXPECTRES, ''), RDID, COLLID, c.NAME, MEASID, f.RECFILEID, f.FILEPATH, "
                       "NVL(f.RECDRIVENDIST, 0), NVL(f.ENDABSTS - f.BEGINABSTS, 0), r.VALUE, u.LABEL, "
                       "i.FORMAT, i.IMAGE "
                       "FROM VAL_RESULT r INNER JOIN VAL_RESULTDESCRIPTOR d USING(RDID) "
                       "INNER JOIN VAL_RESULTTYPES y USING(RESTYPEID) "
                       "INNER JOIN GBL_UNITS u USING(UNITID) "
                       "LEFT JOIN VAL_ASSESSMENT v USING(RESASSID) "
                       "LEFT JOIN GBL_ASSESSMENT_STATE a USING(ASSSTID) "
                       "LEFT JOIN CAT_COLLECTIONS c USING(COLLID) "
                       "LEFT JOIN CAT_FILES f USING(MEASID) "
                       "LEFT JOIN VAL_RESULTIMAGE i USING(RESID) "
                       "WHERE RESID IN (%s) ORDER BY RESID" % sql[1])

                resattrs = ["_myId", "_restype", "_name", "_desc", "_state", "_asId", "_comment", "_issue",
                            "_asmdt", "_doorsurl", "_doorsid", "_expected", "_rdid"]

                try:
                    sqa['lob'] = 23
                    attrs, coll, driven, values = [None] * 13, [None] * 5, [None] * 2, [0] * 4
                    attrs[0], attrs[1], attrs[2], attrs[3], attrs[4], attrs[5], attrs[6], attrs[7], attrs[8], \
                        attrs[9], attrs[10], attrs[11], attrs[12], coll[0], coll[1], coll[2], coll[3], coll[4], \
                        driven[0], driven[1], values[0], values[1], values[2], values[3] = \
                        zip(*self._db.execute(sqi, **sqa))
                    # lock=["v.ASSSTID", "v.ASSCOMMENT", "v.TRACKING_ID", "v.ASSDATE"] if self._lock else False
                except:
                    pass
                else:
                    # attrs[5] = [str(a) for a in attrs[5]] # comment
                    # attrs[10] = [str(a) for a in attrs[10]] # expected

                    # for cidx in xrange(len(self._childs)):
                    for cidx in sorted(set(attrs[0])):
                        # if self._childs[cidx][1] not in (Result.CASE, Result.STEP):
                        #    continue

                        ridx = next(k for k in xrange(0, len(attrs[0])) if attrs[0][k] == cidx)
                        dict_ = {resattrs[k]: attrs[k][ridx] for k in xrange(len(resattrs))}
                        dict_["_collection"] = [coll[k][ridx] for k in xrange(5)]
                        dict_["_driven"] = [driven[k][ridx] for k in xrange(2)]

                        val, lbl, img = values[0][ridx], values[1][ridx], None
                        if values[2][ridx] is not None:
                            try:
                                img = values[3][ridx]
                                sio = StringIO(img)
                                with GzipFile(mode='rb', fileobj=sio) as gz:
                                    img = loads(gz.read())
                            except:
                                pass
                            finally:
                                sio.close()
                        if lbl not in (None, 'None', ''):
                            val = self._pyfy(str(val) + "*" + self._replace_unit(lbl))

                        dict_.update({"_value": val, "_format": values[2][ridx], "_image": img,
                                      "_observer": self._observer})

                        # now add the whole as case or step
                        restype = Result.CASE if attrs[1][ridx] == 'VAL_TESTCASE' else Result.STEP
                        cls = Result.CLSUB[restype]
                        self._childs.append(cls(connection=self._db, name=cidx, parent=self,  # lock=self._lock,
                                                showall=self._showall, resulttype=restype, filter=self._filter,
                                                attribs=dict_))

                        # self._childs[cidx] = cls(self._db, name=self._childs[cidx][0], parent=(self._myId, None),
                        #                         resulttype=self._childs[cidx][1], filter=self._filter, attribs=dict_)

    def _get_sql_det(self, select, joinstr, asmtbind):
        """build up SQL query to retrieve events and results
        """
        sql = [None, None]
        sqa = {}
        fsplt = [6, 3]
        fltr = [' OR '.join([("t.NAME LIKE '%s'" % f[3:])
                             for f in self._filter if f.startswith('et.')]),
                ' OR '.join([("y.NAME LIKE '%s' AND a.VALUE %s" % (f.split(' ', 1)[0][4:], f.split(' ', 1)[1]))
                             for f in self._filter if f.startswith('eat.')]),
                ' OR '.join([("SE%s" % f[2:]) for f in self._filter if f.startswith('e.ID')]),
                ' OR '.join([("f.%s" % f[2:]) for f in self._filter if f.startswith('g.RECFILEID')]),
                ' OR '.join([("s.NAME %sLIKE '%s' ESCAPE '/'" % ("" if f.find(' != ') < 0 else "NOT ",
                                                                 f[f.rfind('= ') + 2:].replace("_", "/_")))
                             for f in self._filter if f.startswith('g.ASSESSMENT')]),
                ' OR '.join([("v.TRACKING_ID %sLIKE '%s' ESCAPE '/'" % ("" if f.find(' != ') < 0 else "NOT ",
                                                                        f[f.rfind('= ') + 2:].replace("_", "/_")))
                             for f in self._filter if f.startswith('g.ISSUE')]),
                ' OR '.join([("t.NAME LIKE '%s' ESCAPE '/'" % f[3:].replace("_", "/_"))
                             for f in self._filter if f.startswith('rt.')])]

        fltr = [(" AND (%s)" % f) if len(f) else "" for f in fltr]
        flen = [len(f) > 0 for f in fltr]
        join = "LEFT" if self._showall else "INNER"

        preslct = ("WITH RECUR(RESID, RDID) AS (SELECT RESID, RDID FROM VAL_RESULT WHERE RESID = :resid UNION ALL "
                   "SELECT NULL, d.RDID FROM VAL_RESULTDESCRIPTOR d INNER JOIN RECUR r ON d.PARENT = r.RDID "
                   "WHERE d.PARENT $SC) ")
        sqa['resid'] = self._myId

        # stop condition either way
        preslct = preslct.replace("$SC", ("IS NOT NULL" if self._parent.rdid == 'NULL'
                                          else ("!= %d" % self._parent.rdid)))

        if (not any(flen[fsplt[1]:]) or any(flen[:fsplt[0]])) and "x.EVENTS" in self._filter:
            sql[0] = ("SELECT DISTINCT %s FROM VAL_EVENTS e INNER JOIN VAL_EVENTTYPES t USING(EVENTTYPEID) "
                      "$SA$ JOIN CAT_FILES f USING(MEASID) INNER JOIN VAL_EVENTDETAILS USING(SEID) "
                      "INNER JOIN VAL_EVENTATTR a USING(EDID) INNER JOIN VAL_EVENTATTRTYPES y USING(ATTRTYPEID) "
                      "$SA$ JOIN VAL_ASSESSMENT v USING(RESASSID) $SA$ JOIN GBL_ASSESSMENT_STATE s USING(ASSSTID) "
                      "WHERE RDID IN (SELECT RDID FROM RECUR WHERE RESID IS NULL)%s AND TRID = :trid"
                      % (select[0], asmtbind))
            sqa['trid'] = self._parent.id
            sql[0] = sql[0].replace("$SA$", join)
            for i in xrange(fsplt[0]):
                sql[0] += fltr[i]

        if (any(flen[fsplt[1]:]) or not any(flen[:fsplt[0]])) and "x.RESULTS" in self._filter:
            sql[1] = ("SELECT DISTINCT %s FROM VAL_RESULT r INNER JOIN VAL_RESULTDESCRIPTOR d USING(RDID) "
                      "INNER JOIN VAL_RESULTTYPES t USING (RESTYPEID) $SA$ JOIN CAT_FILES f USING(MEASID) "
                      "$SA$ JOIN VAL_ASSESSMENT v USING(RESASSID) $SA$ JOIN GBL_ASSESSMENT_STATE s USING(ASSSTID) "
                      "WHERE RDID IN (SELECT RDID FROM RECUR WHERE RESID IS NULL)%s AND TRID = :trid"
                      % (select[1], asmtbind))
            # "WHERE r.TRID = %d AND d.PARENT = (SELECT RDID FROM VAL_RESULTDESCRIPTOR d "
            # "INNER JOIN VAL_RESULT r USING(RDID) WHERE r.RESID = %d)%s"
            # % (select[1], self._parent.id, self._myId, asmtbind))
            sqa['trid'] = self._parent.id
            sql[1] = sql[1].replace("$SA$", join)
            for i in xrange(fsplt[1], len(flen)):
                sql[1] += fltr[i]

        if joinstr is not None:
            sql = preslct + joinstr.join([s for s in sql if s is not None])
        else:
            sql = [(None if s is None else (preslct + s)) for s in sql]

        return sql, sqa

    @classmethod
    def reg_sub(cls, theid):
        """used for subclass registration as we need to return proper child classes for iteration
        """
        def inner(subcls):
            """update class dict"""
            cls.CLSUB[theid] = subcls
            return subcls
        return inner

    @staticmethod
    def _pyfy(val):
        """syms the pyfy"""
        return sympify(val).subs(SSUBS)

    @staticmethod
    def _replace_unit(val, forward=True):
        """handles deg, rad, ..."""
        i, k = (0, 1) if forward else (1, 0)
        for r in (("deg", "degrees"), ("rad", "radians"), ("%", "percent"), ("100km", "(100*km)")):
            val = val.replace(r[i], r[k])
        return val

    def commit(self):
        """commit changes to DB"""
        if self._type in (Result.STEP, Result.EVENT):
            self._oldState, self._oldComment = self._state, self._comment
            self._oldIssue, self._oldAsmdt = self._issue, self._asmdt
        else:
            for i in xrange(len(self._childs)):
                if type(self._childs[i]) not in (tuple, list):
                    self._childs[i].commit()

    def rollback(self):
        """rollback changes done, mainly from assessment"""
        if self._type in (Result.STEP, Result.EVENT):
            self._state, self._comment = self._oldState, self._oldComment
            self._issue, self._asmdt = self._oldIssue, self._oldAsmdt
        else:
            for i in xrange(len(self._childs)):
                if type(self._childs[i]) not in (tuple, list):
                    self._childs[i].rollback()

    @property
    def ID(self):
        """:return: my own id"""
        return self._myId

    @property
    def type(self):
        """:return: my type, RUN, CASE or STEP"""
        return self._restype

    @property
    def name(self):
        """:return: my name"""
        return self._name

    @property
    def resType(self):
        """:return: result type"""
        return self._type

    @property
    def value(self):
        """returns the step value"""
        return self._value

    @value.setter
    def value(self, val):
        """sets / updates the value"""
        self._set_value(val, None, None)

    @property
    def format(self):
        """returns format of value"""
        return None if self._type == Result.RUN else self._format

    @property
    def image(self):
        """returns the image"""
        return None if self._type == Result.RUN else self._image

    @property
    def desc(self):
        """:return: my description"""
        return self._desc

    @property
    def assessment(self):
        """provided for completeness to serve the other way round"""
        return self._state, self._comment, self._issue, self._asmdt

    @assessment.setter
    def assessment(self, value):
        """updates the whole assessment: (state, comment, issue), use None for 'not to be updated'"""
        sql = "UPDATE VAL_ASSESSMENT SET ASSDATE = $CT"
        sqa = {'rea': self._asId}
        for col, arg, val in zip(("ASSSTID", "ASSCOMMENT", "TRACKING_ID"),
                                 ("asid", "comm", "trid"),
                                 (self._check_gbl_state(value[0]) if value[0] is not None else None,
                                  value[1] if value[1] != '' else '-', value[2])):
            if val is not None:
                sql += (", %s = :%s" % (col, arg))
                sqa[arg] = val
        self._db.execute(sql + " WHERE RESASSID = :rea", **sqa)
        if value[0] is not None:
            self._state = value[0]
        if value[1] is not None:
            self._comment = value[1]
        if value[2] is not None:
            self._issue = value[2]

    @property
    def expected(self):
        """returns the reference value"""
        return self._expected

    @property
    def reccat(self):
        """returns the collection and measurement used"""
        return self._collection

    @property
    def doors(self):
        """returns the doors URL"""
        return self._doorsid, self._doorsurl

    @property
    def mtsIssues(self):
        """returns details about reported MTS tasks"""
        # TODO: add proper MKS issue description
        return []

    @property
    def driven(self):
        """return driven distance and time [s]"""
        if self._type == Result.RUN:
            if len(self._driven) == 0:
                sql = ("SELECT NVL(RECDRIVENDIST, 0), (ENDABSTS - BEGINABSTS) FROM CAT_FILES WHERE MEASID IN "
                       "(SELECT DISTINCT MEASID FROM (SELECT TRID, MEASID FROM VAL_RESULT UNION SELECT TRID, MEASID "
                       "FROM VAL_EVENTS) WHERE TRID = :trid)")
                self._driven = [sum(i) for i in zip(*self._db.execute(sql, trid=self._myId))]
                if self._driven == []:
                    self._driven = [0, 0]
            return self._driven
        else:
            return self._driven

    @property
    def files(self):
        """return files having processed"""
        if self._type == Result.RUN:
            return self._db.execute("SELECT COUNT(DISTINCT MEASID) FROM (SELECT TRID, MEASID FROM VAL_RESULT UNION "
                                    "SELECT TRID, MEASID FROM VAL_EVENTS) WHERE TRID = :trid", trid=self._myId)[0][0]
        else:
            return 0 if self._collection[3] is None else 1

    @property
    def connection(self):
        """:return database connection"""
        return self._db

    def __getattr__(self, name):
        """using for backward compatible things, like stk reports"""
        bak = Result.GETATTR[name]
        if bak[0] == "__iter__":
            return self
        elif bak[0] == "__id__":
            return self._myId if self._type == Result.RUN else self.doors[0]
        elif bak[0] == "__len__":
            return len(self)
        else:
            attr = getattr(self, bak[0]) if len(bak) == 1 else getattr(self, bak[0])[bak[1]]
            return "" if attr is None else attr

    @staticmethod
    def __setattribute__(name, value):
        """set internal variables"""
        pass


class TestSuite(Result):
    """A test suite is the super class for test runs.
    """
    def __init__(self, project, name, checkpoint, observer, **kwargs):
        """a test suite is highest of any test data being able to save to DB.
        here we start:
          give the suite a connection string or BaseDB derived object,
          if connection string given, add dbPrefix parameter being able to resolve
          proper table names.
          Well, a suite got a name, a string as being the checkpoint identifier
          where tests are being performed and a name for testing observer.

          Classes TestSuite, TestRun, TestCase and TestStep

        :param connection: (connection string, dbPrefix) or predefined CONN_STRING
        :param project: project name (run)
        :param name: descriptive name of run
        :param checkpoint: checkpoint string to be set
        :param observer: name of observer doing evaluation
        :keyword collection: collection to use (case, step)
        """
        Result.__init__(self, project=project, name=name, checkpoint=checkpoint, observer=observer, **kwargs)

    @property
    def checkpoint(self):
        """:return: my description"""
        return self._checkPoint

    @property
    def project(self):
        """:return: project name"""
        return self._prj

    @property
    def locked(self):
        """:return: lock status of run"""
        return self._isLocked

    def add_run(self, **kwargs):
        """take care of specials for a suite, only runs can be appended"""
        kwargs['type'] = Result.RUN  # overwrite, just in case
        return Result._append(self, mode=Result.WRITE, **kwargs)

    def commit(self):
        """iterate and commit changes to DB"""
        for t in self:
            t.commit()
        self._db.commit()

    def rollback(self):
        """iterate and rollback changes done, mainly used from assessment"""
        for t in self:
            t.rollback()
        self._db.rollback()

    def close(self, commit=True):
        """closes connection
        :param commit: wether to really commit or not (as being called by exit as well)
        """
        self._close(commit)


@Result.reg_sub(Result.RUN)
class TestRun(Result):
    """A test run encapsulates test cases.
    """
    def __init__(self, **kwargs):
        """test runs are contained inside a test suite.
          A run has for sure a name and a string for checkpoint identification.

          Do not derive your run from this class as you get back an instance object
          while iterating through a test suite or when appending a run to a suite via suite.addRun(...)!
        """
        Result.__init__(self, **kwargs)

    @property
    def checkpoint(self):
        """:return: my description"""
        return self._checkPoint

    @property
    def project(self):
        """:return: project name"""
        return self._prj

    def add_case(self, **kwargs):
        """appends a case with following attributes:
        :keyword name: descriptive name
        :keyword desc: description of it
        :keyword state: e.g. 'passed', etc.
        """
        kwargs.pop('type', None)  # remove, just in case
        return Result._append(self, mode=Result.WRITE, **kwargs)

    def copy_from(self, src_run):
        """
        :param src_run: name of run to copy all elements
        """
        src_db = src_run.connection
        # if len(self._table_dicts) == 0:
        #     self._table_dicts = DefDict(None,
        #                                 GBL_USERS=UserTableDict(src_db, self._db, "GBL_USERS"),
        #                                 CAT_FILES=MeasDict(src_db, self._db, "CAT_FILES"),
        #                                 GBL_TESTTYPE=TableDict(src_db, self._db, "GBL_TESTTYPE"),
        #                                 GBL_COMPONENTS=TableDict(src_db, self._db, "GBL_COMPONENTS"),
        #                                 GBL_PROJECT=TableDict(src_db, self._db, "GBL_PROJECT"))

        def recur(other, this):
            """go recursive"""
            kwargs = {k: getattr(other, k) for k in (Result.GETATTR.keys() + [a for a in dir(other) if match("[a-z]", a[0])]) if hasattr(other, k)}
            kwargs.update({"type": other.resType, "mode": Result.WRITE})
            res = this._append(**kwargs)

            for i in other:
                recur(i, res)

        for i in src_run:
            recur(i, self)


@Result.reg_sub(Result.CASE)
class TestCase(Result):
    """A test case encapsulates test steps.
    """
    def __init__(self, **kwargs):
        """test cases are inside test runs.
          A test case has for sure a name, some description if you like and a state, e.g. 'passed' or 'failed'
          optionally, if none given, 'Not_Assessed' will be used.

          Do not derive your case from this class as you get back an instance object
          while iterating through a test run or when appending a case to a run via run.addCase(...)!
        """
        Result.__init__(self, **kwargs)

    def add_step(self, **kwargs):
        """appends a step with following attributes:
        :keyword name: descriptive name
        :keyword desc: description of it
        :keyword value: can be of any type
        :keyword state: e.g. 'passed', etc.
        :keyword reftag: will be put into db as string (reference)
        """
        kwargs['type'] = Result.STEP
        return Result._append(self, mode=Result.WRITE, **kwargs)

    def add_event(self, **kwargs):
        """appends an event
        """
        kwargs['type'] = Result.EVENT
        return Result._append(self, mode=Result.WRITE, **kwargs)


@Result.reg_sub(Result.STEP)
class TestStep(Result):
    """This is the lowest thing: a test step.
    """
    def __init__(self, *args, **kwargs):
        """A test step has for sure a name, some description if you like and a state, e.g. 'passed' or 'failed'
        optionally, if none given, 'Not_Assessed' will be used. And last but not least, a value and unit to be saved.

          Do not derive your step from this class as you get back an instance object
          while iterating through a test case or when appending a step to a case via run.addStep(...)!
        """
        Result.__init__(self, *args, **kwargs)


@Result.reg_sub(Result.EVENT)
class TestEvent(Result):
    """A test case encapsulates test steps.
    """
    def __init__(self, **kwargs):
        """test events are inside test runs.
          A test event has for sure some start/end numbers and more

          Do not derive your case from this class as you get back an instance object
          while iterating through a test case or when appending an event to a case via case.addEvent(...)!
        """
        Result.__init__(self, **kwargs)

    @property
    def attribs(self):
        """return attributes of event
        """
        return self._attrs

    @property
    def start_end(self):
        """return start/end indices of event
        """
        return self._startEnd


"""
CHANGE LOG:
-----------
$Log: result.py  $
Revision 1.1 2018/06/13 07:57:16CEST Mertens, Sven (uidv7805) 
Initial revision
Member added to project /nfs/projekte1/REPOSITORY/Tools/Validation_Tools/Lib_Libraries/STK_ScriptingToolKit/05_Software/04_Engineering/01_Source_Code/stk/db/project.pj
Revision 1.11 2016/02/10 15:02:45CET Mertens, Sven (uidv7805)
sim_name and sort is needed for shared stk's report
Revision 1.10 2016/02/08 09:23:08CET Mertens, Sven (uidv7805)
replacement for oracle specific query
Revision 1.9 2016/01/18 11:16:52CET Mertens, Sven (uidv7805)
reworking some queries using named parameters
Revision 1.8 2015/12/04 14:08:37CET Mertens, Sven (uidv7805)
fixing doors
Revision 1.7 2015/10/20 16:57:54CEST Mertens, Sven (uidv7805)
observer fix
--- Added comments ---  uidv7805 [Oct 20, 2015 4:57:55 PM CEST]
Change Package : 340395:2 http://mks-psad:7002/im/viewissue?selection=340395
Revision 1.6 2015/10/13 16:33:08CEST Mertens, Sven (uidv7805)
asmt state fix
--- Added comments ---  uidv7805 [Oct 13, 2015 4:33:09 PM CEST]
Change Package : 372724:2 http://mks-psad:7002/im/viewissue?selection=372724
Revision 1.5 2015/10/08 18:16:11CEST Mertens, Sven (uidv7805)
leave away lock functionality as not properly validated
--- Added comments ---  uidv7805 [Oct 8, 2015 6:16:12 PM CEST]
Change Package : 372724:2 http://mks-psad:7002/im/viewissue?selection=372724
Revision 1.4 2015/10/01 16:37:49CEST Mertens, Sven (uidv7805)
take care of preselections
--- Added comments ---  uidv7805 [Oct 1, 2015 4:37:50 PM CEST]
Change Package : 372724:2 http://mks-psad:7002/im/viewissue?selection=372724
Revision 1.3 2015/09/18 16:15:13CEST Mertens, Sven (uidv7805)
one more recursion
--- Added comments ---  uidv7805 [Sep 18, 2015 4:15:13 PM CEST]
Change Package : 372724:1 http://mks-psad:7002/im/viewissue?selection=372724
Revision 1.2 2015/06/12 10:07:07CEST Mertens, Sven (uidv7805)
reverting cat_dmt_files_b to cat_files
--- Added comments ---  uidv7805 [Jun 12, 2015 10:07:07 AM CEST]
Change Package : 343183:1 http://mks-psad:7002/im/viewissue?selection=343183
Revision 1.1 2015/06/01 14:12:44CEST Mertens, Sven (uidv7805)
Initial revision
Member added to project /nfs/projekte1/REPOSITORY/Tools/Validation_Tools/LT_LabelTools/VAT_ValidationAssessmentTool/
    05_Software/04_Engineering/01_Source_Code/project.pj
Revision 1.1 2015/04/22 13:38:05CEST Mertens, Sven (uidv7805)
Initial revision
Member added to project /nfs/projekte1/REPOSITORY/Tools/Validation_Tools/LT_LabelTools/VAT_ValidationAssessmentTool/
    05_Software/04_Engineering/01_Source_Code/project.pj
Revision 1.9 2015/03/24 09:54:56CET Mertens, Sven (uidv7805)
fix for global filters
--- Added comments ---  uidv7805 [Mar 24, 2015 9:54:57 AM CET]
Change Package : 318534:4 http://mks-psad:7002/im/viewissue?selection=318534
Revision 1.8 2015/03/18 10:51:52CET Mertens, Sven (uidv7805)
fix: take care of assessment states
--- Added comments ---  uidv7805 [Mar 18, 2015 10:51:53 AM CET]
Change Package : 318534:1 http://mks-psad:7002/im/viewissue?selection=318534
Revision 1.7 2015/03/05 11:29:20CET Mertens, Sven (uidv7805)
pdf creator needs additional info
--- Added comments ---  uidv7805 [Mar 5, 2015 11:29:21 AM CET]
Change Package : 312733:1 http://mks-psad:7002/im/viewissue?selection=312733
Revision 1.6 2015/01/27 14:29:15CET Mertens, Sven (uidv7805)
fix for event or result only filter
--- Added comments ---  uidv7805 [Jan 27, 2015 2:29:15 PM CET]
Change Package : 300091:1 http://mks-psad:7002/im/viewissue?selection=300091
Revision 1.5 2015/01/16 14:05:10CET Mertens, Sven (uidv7805)
empty value for assessment comment not permitted
Revision 1.4 2015/01/13 09:31:14CET Mertens, Sven (uidv7805)
sql query fix
--- Added comments ---  uidv7805 [Jan 13, 2015 9:31:15 AM CET]
Change Package : 294959:1 http://mks-psad:7002/im/viewissue?selection=294959
Revision 1.3 2014/11/24 10:48:42CET Mertens, Sven (uidv7805)
fix for sqlite any data loading prevention
Revision 1.2 2014/11/11 13:43:45CET Mertens, Sven (uidv7805)
misc
Revision 1.1 2014/10/16 14:53:06CEST Mertens, Sven (uidv7805)
Initial revision
Member added to project /nfs/projekte1/REPOSITORY/Base_Development/05_Algorithm/ETK_EngineeringToolKit/
    04_Engineering/VAT_ValidationAssessmentTool/04_Engineering/01_Source_Code/vat/project.pj
Revision 1.15 2014/10/08 13:33:31CEST Mertens, Sven (uidv7805)
adding issue as filter
--- Added comments ---  uidv7805 [Oct 8, 2014 1:33:31 PM CEST]
Change Package : 269564:1 http://mks-psad:7002/im/viewissue?selection=269564
Revision 1.14 2014/10/07 16:55:38CEST Mertens, Sven (uidv7805)
- utc usage,
- user configuable result/event detail retrieval
--- Added comments ---  uidv7805 [Oct 7, 2014 4:55:39 PM CEST]
Change Package : 269564:1 http://mks-psad:7002/im/viewissue?selection=269564
Revision 1.13 2014/09/29 14:24:35CEST Mertens, Sven (uidv7805)
preloading things more effectively
--- Added comments ---  uidv7805 [Sep 29, 2014 2:24:36 PM CEST]
Change Package : 267610:1 http://mks-psad:7002/im/viewissue?selection=267610
Revision 1.12 2014/09/15 13:56:34CEST Mertens, Sven (uidv7805)
speeding up result and event loading
--- Added comments ---  uidv7805 [Sep 15, 2014 1:56:34 PM CEST]
Change Package : 264032:1 http://mks-psad:7002/im/viewissue?selection=264032
Revision 1.11 2014/09/09 15:09:09CEST Mertens, Sven (uidv7805)
adding gbl_component and gbl_testtype support
--- Added comments ---  uidv7805 [Sep 9, 2014 3:09:10 PM CEST]
Change Package : 261716:1 http://mks-psad:7002/im/viewissue?selection=261716
Revision 1.10 2014/09/09 10:40:17CEST Mertens, Sven (uidv7805)
speedup for event retrieval
--- Added comments ---  uidv7805 [Sep 9, 2014 10:40:18 AM CEST]
Change Package : 261716:1 http://mks-psad:7002/im/viewissue?selection=261716
Revision 1.9 2014/09/04 14:40:38CEST Mertens, Sven (uidv7805)
fix for wrong concatenation
--- Added comments ---  uidv7805 [Sep 4, 2014 2:40:39 PM CEST]
Change Package : 261716:1 http://mks-psad:7002/im/viewissue?selection=261716
Revision 1.8 2014/09/04 13:23:00CEST Mertens, Sven (uidv7805)
update according last requirements meeting of 03.09.2014
--- Added comments ---  uidv7805 [Sep 4, 2014 1:23:00 PM CEST]
Change Package : 261716:1 http://mks-psad:7002/im/viewissue?selection=261716
Revision 1.7 2014/06/27 16:04:49CEST Mertens, Sven (uidv7805)
saving childs interim to save reoccuring fetches (speed improvement)
--- Added comments ---  uidv7805 [Jun 27, 2014 4:04:49 PM CEST]
Change Package : 244476:1 http://mks-psad:7002/im/viewissue?selection=244476
Revision 1.6 2014/05/21 21:24:07CEST Mertens, Sven (uidv7805)
- update of treeview when loosing focus,
- commit and rollback option added,
- extra UI menu for sqlite addon,
- play, stop, rew and ffw for acc viewer
--- Added comments ---  uidv7805 [May 21, 2014 9:24:08 PM CEST]
Change Package : 238467:1 http://mks-psad:7002/im/viewissue?selection=238467
Revision 1.5 2014/05/15 15:41:34CEST Mertens, Sven (uidv7805)
fix for main header misalignment
Revision 1.4 2014/05/14 14:27:40CEST Mertens, Sven (uidv7805)
- adding messagebox for sqlite version too low,
- fixing accviewer crash
Revision 1.3 2014/05/13 15:54:41CEST Mertens, Sven (uidv7805)
fix for filtered events: should show results if not filtered as well...
--- Added comments ---  uidv7805 [May 13, 2014 3:54:41 PM CEST]
Change Package : 236402:1 http://mks-psad:7002/im/viewissue?selection=236402
Revision 1.2 2014/05/13 10:10:43CEST Mertens, Sven (uidv7805)
- columns startTS and endTS added,
- added icon to remove sqlite db,
- fix: setup uses vat's version info,
- fix: removing deleted runs.
--- Added comments ---  uidv7805 [May 13, 2014 10:10:43 AM CEST]
Change Package : 236401:1 http://mks-psad:7002/im/viewissue?selection=236401
Revision 1.1 2014/05/09 16:22:13CEST Mertens, Sven (uidv7805)
Initial revision
Member added to project /nfs/projekte1/REPOSITORY/Base_Development/05_Algorithm/ETK_EngineeringToolKit/04_Engineering/
    VAT_ValidationAssessmentTool/04_Engineering/01_Source_Code/project.pj
"""
