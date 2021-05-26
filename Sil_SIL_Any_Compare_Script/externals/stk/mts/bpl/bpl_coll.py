"""
bpl_coll.py
-----------

class for collection (BatchPlayList) handling

:org:           Continental AG
:author:        Sven Mertens

:version:       $Revision: 1.3 $
:contact:       $Author: Mertens, Sven (uidv7805) $ (last change)
:date:          $Date: 2017/12/12 15:02:49CET $
"""
# - Python imports -----------------------------------------------------------------------------------------------------
try:
    from types import StringTypes
except ImportError:
    StringTypes = (str,)

# - import HPC modules -------------------------------------------------------------------------------------------------
from .bpl_base import BplReaderIfc, BplException, BplListEntry


# - classes ------------------------------------------------------------------------------------------------------------
class BPLColl(BplReaderIfc):
    """
    Specialized BPL Class which handles only reading of a collection.
    This class is not a customer Interface, it should only be used internal of hpc.
    """
    def read(self):
        """
        Read the whole content of the Batch Play List into internal storage,
        and return all entries as a list.

        :return:        List of Recording Objects
        :rtype:         BplList
        """
        from ...db.catalog import Collection, CollManager, CollException

        self.clear()

        db = self._kwargs.get("db", "VGA_PWR")
        args = {"name": self.filepath} if type(self.filepath) in StringTypes else \
            {"name": self.filepath[0], "label": self.filepath[1]}

        try:
            with Collection(db, mode=CollManager.READ, **args) as coll:
                def recur(icoll):
                    for i in icoll:
                        if i.type == CollManager.COLL:
                            recur(i)
                        elif i.type == CollManager.SHARE:
                            recur(Collection(db, name=i.name, label=i.label))
                        else:
                            ble = BplListEntry(i.name)
                            beg, end = i.beginrelts, i.endrelts
                            if any([beg, end]):
                                try:
                                    ble.append(beg, end, (True, True,))
                                except:
                                    pass
                            self.append(ble)

                recur(coll)
        except CollException as ex:
            raise BplException(ex.message, 2)

        return self

    def write(self):
        """writing to a collection is not supported!
        """
        from ...db.catalog import Collection, CollManager, CollException

        db = self._kwargs.get("db", "VGA_PWR")
        args = {"name": self.filepath} if type(self.filepath) in StringTypes else \
            {"name": self.filepath[0], "label": self.filepath[1]}

        try:
            with Collection(db, mode=CollManager.WRITE, parent=self._kwargs["parent"], **args) as coll:
                for i in self:
                    coll.add_rec(name=str(i))

        except CollException as ex:
            raise BplException(ex.message, 2)
        except Exception as ex:
            raise


"""
CHANGE LOG:
-----------
$Log: bpl_coll.py  $
Revision 1.3 2017/12/12 15:02:49CET Mertens, Sven (uidv7805) 
provide a write functionality
Revision 1.2 2017/12/11 17:11:37CET Mertens, Sven (uidv7805) 
import inside
Revision 1.1 2017/12/11 15:32:13CET Mertens, Sven (uidv7805) 
Initial revision
Member added to project /nfs/projekte1/REPOSITORY/Tools/Validation_Tools/Lib_Libraries/STK_ScriptingToolKit/
    05_Software/04_Engineering/01_Source_Code/stk/mts/bpl/project.pj
"""
