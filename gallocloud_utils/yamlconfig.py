import yaml, re, os

def load_config_from_yaml(content=None, default_filepath=None, envs=None, format=None):
    if not envs:
        envs = os.environ

    if not format:
        format = lambda x: x

    loader = yaml.SafeLoader

    if not content:
        filepath = envs.get('CONFIG_FILE', default_filepath)
        f = open(filepath)
        content = f.read()
        f.close()

    pattern = re.compile('.*?\${(\w+)(?:\|(\w+))?}.*?')
    pattern2 = re.compile('\${(\w+)(?:\|(\w+))?}')
    pattern3 = re.compile('^\${(\w+)(?:\|(\w+))?}$')

    def constructor_env_variables(loader, node):
        value = loader.construct_scalar(node)
        match = pattern.findall(value)  # to find all env variables in line
        if match:
            full_value = value
            for g in match:
                env, type = g
                if not type:
                    type = 'str'

                val = envs.get(env)

                if val == None:
                    raise Exception('Env %s not found' % env)

                if type != 'str':

                    if not pattern3.match(value):
                        raise Exception('cast only on full value')

                    if (type == 'int'):
                        return int(val)
                    if (type == 'float'):
                        return float(val)
                    if type == 'bool':
                        if not val or val.lower() == 'false' or val == '0':
                            return False
                        return True

                    raise Exception('Invalid cast')


                full_value = pattern2.sub(val, full_value, 1)
            return full_value
        return value
    tag = '!env'
    loader.add_implicit_resolver(tag, pattern, None)
    loader.add_constructor(tag, constructor_env_variables)

    return format(yaml.load(content, Loader = loader))
