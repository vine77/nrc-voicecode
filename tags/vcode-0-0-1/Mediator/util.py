"""Various utility functions"""


import getopt, os, re, stat, sys

def dict_merge(dict1, dict2):
    """Merges two dictionaries
    
    Merges *{ANY: ANY} dict1* and *{ANY: ANY} dict2* and returns the
    result *{ANY: ANY} dict3*.

    If a key exists in both *dict1* and *dict2*, the value in *dict1*
    will be used for *dict3*
    """
    dict3 = dict2
    for an_item in dict1.items():
        key, val = an_item
        dict3[key] = val
    return dict3



def gopt(opt_defs, cmd=sys.argv[1:]):
    """High level wrapper around *getopt.getop*.

    *removes first argument from *cmd* when parsing from *sys.argv*
        
    *returned options are stored in a dictionary

    *dashes ('-') are removed from the option name in that dictionary

    *returns None and outputs error messages if invalid option

    *allows to define default values for options
        
    **INPUTS**
        
    *[STR]* cmd=sys.argv[1:] -- list of options and arguments to be parsed. 
        
    *[STR, ANY, ...]* opt_defs -- defines the valid options (short and
    long). The list is an alternate sequence of option name and
    default value. If the name ends with *=*, it means the option
    requires a value. If the name is a single letter, it's a short
    option. The defaul value is compulsory, even for options that
    don't require a value (can be used to set the switch to on or
    off by default).
        

    **OUTPUTS**
        
    *opts, args* -- *opts* is a dictionary of options names and
    values. *args* is the list of arguments.
    """
    #
    # Set default values of options
    #
    index = 0
    opt_dict = {}
    while (index < len(opt_defs)):
        opt_name = opt_defs[index]
        opt_default = opt_defs[index + 1]
        opt_name = re.match('^(.*?)(=*)$', opt_name).groups()[0]        
        opt_dict[opt_name] = opt_default
        index = index + 2


    #
    # Parse command line
    #
    args = []
    short_opts = ''
    long_opts = []

    index = 0
    while (index < len(opt_defs)):
        opt_name = opt_defs[index]
        opt_default = opt_defs[index + 1]
        index = index + 2
        match = re.match('^(.)(.*?)(=*)$', opt_name)
        opt_name = match.groups()[0]+ match.groups()[1]
        is_long = 0
        requires_val = 0
        if (match.groups()[1] != ''):
            is_long = 1
        if (match.groups()[2] != ''):
            requires_val = 1
            
        if (is_long):
            long_opts = long_opts + [opt_name + match.groups()[2]]
        else:
            short_opts = short_opts + opt_name
            if (requires_val):
                short_opts = short_opts + ':'
    options, args = getopt.getopt(cmd, short_opts, long_opts)
    for an_opt in options:
        opt_name = an_opt[0]
        a_match = re.match('^(-*)(.*)$', opt_name)
        opt_name = a_match.groups()[1]
        if (a_match.groups()[0] == '-'):
            #
            # getopt.getopt returns None as the value for short options
            # but we want it to be 1, otherwise it makes it look like the
            # options was off
            #
            # In getopt.getopt, that didn't matter because the mere presence
            # of the option name indicates it is on.
            #
            # In util.gopt, all options have an entry in the returned
            # dictionary, and its value indicates whether it's on or off
            #
            opt_val = 1
        else:
            opt_val = an_opt[1]
        opt_dict[opt_name] = opt_val

#    print "-- gopt: opt_dic=%s, args=%s" % (str(opt_dict)    , str(args))        
    return opt_dict, args



def last_mod(f_name):
    """Returns the time at which a file was last modified.

    *STR f_name* is the path of the file.

    if *f_name* doesn't exist, returns 0.
    """

    try:
        stats = os.stat(f_name)
        time = stats[stat.ST_MTIME]
    except OSError:
        time = 0
        
    return time
