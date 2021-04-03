import yaml, re, os

def load_config_from_yaml(content, envs=None, formatter=None):
    if not envs:
        envs = os.environ

    if not formatter:
        formatter = lambda x: x

    loader = yaml.SafeLoader

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

                val = envs.get(env, env)

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

    return formatter(yaml.load(content, Loader = loader))
