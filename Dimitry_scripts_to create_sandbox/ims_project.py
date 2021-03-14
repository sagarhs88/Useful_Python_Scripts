from enum import Enum


class IMSProject(Enum):
    MFC431TA19 = 1
    MFC431LO19 = 2
    AL_ARS510TA19 = 3

    @staticmethod
    def from_checkpoint(checkpoint):
        for project in IMSProject:
            if checkpoint.startswith(project.name):
                return project

        raise ValueError('Snapshot label {} belongs to an unknown project'.format(checkpoint))

    @property
    def path(self):
        if self == IMSProject.MFC431TA19:
            return '/ADAS/SW/Projects/MFC431x/MFC431TA19/project.pj'

        if self == IMSProject.MFC431LO19:
            return '/ADAS/SW/Projects/MFC431x/MFC431LO19/project.pj'

        if self == IMSProject.AL_ARS510TA19:
            return '/nfs/projekte1/PROJECTS/SMR400/06_Algorithm/project.pj'

        return None

    @property
    def mts_directory(self):
        if self in [IMSProject.MFC431TA19, IMSProject.MFC431LO19]:
            return 'MTS/05_Testing/MTS'

        if self == IMSProject.AL_ARS510TA19:
            return '05_Testing/06_Test_Tools'

        return None


