# -*- coding: utf-8 -*-
""" Configuration management """
import config_file_parser
import command_line_parser

DEFAULT_OPTIONS = {
    'global': {
        # Command line only
        'config': None,
        'daemon': False,
        'dry_run': False,

        # [global]
        'region': 'us-east-1',
        'aws_access_key_id': None,
        'aws_secret_access_key': None,
        'check_interval': 300
    },
    'logging': {
        # [logging]
        'log_file': None,
        'log_level': 'info',
    },
    'table': {
        'reads_lower_threshold': 30,
        'reads_upper_threshold': 90,
        'increase_reads_with': 50,
        'decrease_reads_with': 50,
        'writes_lower_threshold': 30,
        'writes_upper_threshold': 90,
        'increase_writes_with': 50,
        'decrease_writes_with': 50,
        'min_provisioned_reads': None,
        'max_provisioned_reads': None,
        'min_provisioned_writes': None,
        'max_provisioned_writes': None,
        'allow_scaling_down_reads_on_0_percent': False,
        'allow_scaling_down_writes_on_0_percent': False,
        'always_decrease_rw_together': False,
        'maintenance_windows': None,
    }
}


def get_configuration():
    """ Get the configuration from command line and config files """
    # This is the dict we will return
    configuration = {
        'global': {},
        'logging': {},
        'tables': {}
    }

    # Read the command line options
    cmd_line_options = command_line_parser.parse()

    # If a configuration file is specified, read that as well
    if 'config' in cmd_line_options:
        conf_file_options = config_file_parser.parse(cmd_line_options['config'])
    else:
        conf_file_options = None

    # Extract global config
    configuration['global'] = __get_global_options(
        cmd_line_options,
        conf_file_options)

    # Extract logging config
    configuration['logging'] = __get_logging_options(
        cmd_line_options,
        conf_file_options)

    # Extract table configuration
    # If the --table cmd line option is set, it indicates that only table
    # options from the command line should be used
    if 'table_name' in cmd_line_options:
        configuration['tables'] = __get_cmd_table_options(cmd_line_options)
    else:
        configuration['tables'] = __get_config_table_options(conf_file_options)

    return configuration


def __get_cmd_table_options(cmd_line_options):
    """ Get all table options from the command line

    :type cmd_line_options: dict
    :param cmd_line_options: Dictionary with all command line options
    :returns: dict -- E.g. { 'table_name': {} }
    """
    table_name = cmd_line_options['table_name']
    options = { table_name: {} }

    for option in DEFAULT_OPTIONS['table'].keys():
        options[table_name][option] = DEFAULT_OPTIONS['table'][option]

        if option in cmd_line_options:
            options[table_name][option] = cmd_line_options[option]

    return options


def __get_config_table_options(conf_file_options):
    """ Get all table options from the config file

    :type conf_file_options: dict
    :param conf_file_options: Dictionary with all config file options
    :returns: dict -- E.g. { 'table_name': {} }
    """
    options = {}

    for option in DEFAULT_OPTIONS['table'].keys():
        options[table_name][option] = DEFAULT_OPTIONS['table'][option]

        if option in cmd_line_options:
            options[table_name][option] = cmd_line_options[option]

    return options


def __get_global_options(cmd_line_options, conf_file_options=None):
    """ Get all global options

    :type cmd_line_options: dict
    :param cmd_line_options: Dictionary with all command line options
    :type conf_file_options: dict
    :param conf_file_options: Dictionary with all config file options
    :returns: dict
    """
    options = {}

    for option in DEFAULT_OPTIONS['global'].keys():
        options[option] = DEFAULT_OPTIONS['global'][option]

        if option in conf_file_options:
            options[option] = conf_file_options[option]

        if option in cmd_line_options:
            options[option] = cmd_line_options[option]

    return options


def __get_logging_options(cmd_line_options, conf_file_options=None):
    """ Get all logging options

    :type cmd_line_options: dict
    :param cmd_line_options: Dictionary with all command line options
    :type conf_file_options: dict
    :param conf_file_options: Dictionary with all config file options
    :returns: dict
    """
    options = {}

    for option in DEFAULT_OPTIONS['logging'].keys():
        options[option] = DEFAULT_OPTIONS['logging'][option]

        if option in conf_file_options:
            options[option] = conf_file_options[option]

        if option in cmd_line_options:
            options[option] = cmd_line_options[option]

    return options


def check_rules(configuration):
    """ Do some basic checks on the configuraion """
    # Check that increase_writes_with is not > 100
    if configuration['increase_writes_with'] > 100:
        print(
            'You can not increase the table throughput with more '
            'than 100% at a time. Setting --increase-writes-with to 100.')
        configuration['increase_writes_with'] = 100

    # Check that increase_reads_with is not > 100
    if configuration['increase_reads_with'] > 100:
        print(
            'You can not increase the table throughput with more '
            'than 100% at a time. Setting --increase-reads-with to 100.')
        configuration['increase_reads_with'] = 100

    return configuration
