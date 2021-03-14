import os
import shutil
import stat
import subprocess

from checkout_config import CheckoutConfig, checkout_config_for_project
from ims_project import IMSProject


def project_file(subsandbox):
    return os.path.join(subsandbox, 'project.pj')


def touch_parent_subsandboxes(root_sandbox_dir, target_subsandox_dir):
    path_components = target_subsandox_dir.split(os.path.sep)
    subsandbox = root_sandbox_dir

    for component in path_components:
        subsandbox = os.path.join(subsandbox, component)

        if os.path.exists(subsandbox):
            continue

        print('>>> Touching subsandbox: {}'.format(subsandbox))
        subprocess.check_call(['si', 'resync',
                               '--norecurse',
                               project_file(subsandbox)])


def create_shortcut(source_path, target_path):
    import win32com.client
    shell = win32com.client.Dispatch("WScript.Shell")
    shortcut = shell.CreateShortCut(source_path)
    shortcut.Targetpath = target_path
    shortcut.save()


def copy_dir_owerwriting(source_dir, dest_dir):
    for root, dirs, files in os.walk(source_dir):
        relative_parent_dir = root.replace(source_dir, '').lstrip(os.sep)
        dst_parent_dir = os.path.join(dest_dir, relative_parent_dir)

        if not os.path.exists(dst_parent_dir):
            os.mkdir(dst_parent_dir)

        for file in files:
            dst = os.path.join(dst_parent_dir, file)
            if os.path.exists(dst):
                # TODO: do a proper force-copy instead of removing read-only flag first
                os.chmod(dst, stat.S_IWRITE)

            shutil.copy(os.path.join(root, file), dst)


def checkout_sandbox(checkpoint, source_parent_dir, checkout_config):
    sandbox_dir = os.path.join(os.path.normpath(source_parent_dir), checkpoint)

    if not os.path.exists(sandbox_dir):
        print('>>> Creating build sandbox for revision {} \n\tat: {} \n\tproject: {}'
              .format(checkpoint, sandbox_dir, checkout_config.ims_project))
        subprocess.check_call(['si', 'createsandbox',
                               '--norecurse',
                               '--nopopulate',
                               '--project={}'.format(checkout_config.ims_project),
                               '--projectRevision={}'.format(checkpoint),
                               sandbox_dir])
    else:
        # TODO: if directory exists, check that it contains the right sandbox
        print('>>> Skipping sandbox creation - sandbox directory already exists at: {}'.format(sandbox_dir))

    for subdir in checkout_config.resynced_subdirs:
        print('>>> Resyncing subproject contents for subdirectory {}'.format(subdir))
        subdir = os.path.normpath(subdir)

        touch_parent_subsandboxes(root_sandbox_dir=sandbox_dir, target_subsandox_dir=subdir)

        filters = ['--filter=!file:{}'.format(fmask) for fmask in checkout_config.excluded_filemasks]
        args = ['si', 'resync', '--recurse']
        args.extend(filters)
        args.append(project_file(os.path.join(sandbox_dir, subdir)))

        return_code = subprocess.call(args)
        print('>>> Finished resyncing {} with return code {}'.format(subdir, return_code))

    print('>>> Unlocking readonly configs')
    for relative_path in checkout_config.files_to_unlock:
        abs_path = os.path.join(sandbox_dir, os.path.normpath(relative_path))
        os.chmod(abs_path, stat.S_IWRITE)

    print('>>> Making shortcuts')
    for link_source, link_target in checkout_config.shortcuts:
        abs_source_path = os.path.join(sandbox_dir, os.path.normpath(link_source))
        abs_target_path = os.path.join(sandbox_dir, os.path.normpath(link_target))
        create_shortcut(abs_source_path, abs_target_path)

    print('>>> Applying uncommitted changes')
    script_dir = os.path.dirname(os.path.abspath(__file__))
    uncommited_changes_dir = os.path.join(script_dir, 'uncommited_changes', checkout_config.project_name)
    copy_dir_owerwriting(uncommited_changes_dir, sandbox_dir)

    print('>>> Performing a post checkout action')
    if config.post_checkout_action:
        config.post_checkout_action(sandbox_dir, checkpoint)


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser('Checkout a build sandbox for a given MFC431TA19, MFC431LO19 or ARS510TA19 checkpoint')
    parser.add_argument('checkpoint', help='Revision or label of a checkpoint to be checked out')
    args = parser.parse_args()

    project = IMSProject.from_checkpoint(args.checkpoint)
    config = checkout_config_for_project(project)
    checkout_sandbox(args.checkpoint, source_parent_dir=os.getcwd(), checkout_config=config)


