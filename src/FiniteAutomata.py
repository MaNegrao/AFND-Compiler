class FiniteAutomata(object):
    # default settings
    __initial_state = 0
    __error_state = -1
    __alphabet = []
    __fa = {}
    __next_state = 0

    __input_folder = 'set'

    __tokens_file = 'tokens.csv'
    __gramma_file = 'gramma.in'

    def __init__(self):
        self.map_gramma()
        self.map_tokens()
        self.show()

    def get_avaible_state(self, state=None):
    if state is None:
        state = self.__NEXT_NEW_STATE
    else:
        state += 1
    try:
        while self.__FA[state]['final']:
            state += 1
    except:
        pass
    return state

    def create_state(self, state, final=False, parents=[]):
        if not state in self.__fa:
            self.__fa[state] = {'final': final, 'parents': parents}
            self.__next_state += 1
            for char in self.__alphabet:
                self.__fa[state][char] = []
        elif not self.__fa[state]['final']:
            self.__fa[state]['final'] = final

    def append_char(self, char):
        if not char in self.__alphabet:
            self.__alphabet.append(char)
            for state in self.__fa:
                self.__fa[state][char] = []

    def create_transition(self, state, char, next_state):
        if type(self.__fa[state][char]) == list:
            if next_state not in self.__fa[state][char]:
                self.__fa[state][char].append(next_state)
    
    def map_gramma(self):
        try:
            file = open(self.__input_folder+'/'+self.__gramma_file, 'r')
            for gramma in file:
                # Removing unused characters
                gramma = gramma.replace('\n', '')
                state, productions = gramma.split('::=')
                productions = productions.split('|')
                state = int(state.replace('<', '').replace('>', ''))
                
                self.create_state(state)

                for prod in productions:
                    char = ''
                    next_state = None
                    is_char = True

                    for c in prod:
                        if c == '<' and is_char:
                            next_state = c
                            is_char = False
                        elif c == '>' and not is_char:
                            next_state += c
                            is_char = True
                        elif not is_char:
                            next_state += c
                        else:
                            char = c
                    self.append_char(char)

                    if next_state:
                        next_state = int(next_state.replace('<', '').replace('>', ''))
                        self.create_state(next_state)
                        self.create_transition(state, char, next_state)
                    else:
                        self.__fa[state]['final'] = True
        except:
            pass

    def map_tokens(file): 
        try:
            file = open(self.__input_folder+'/'+self.__tokens_file, 'r')
            for token in file:    
                token = token.replace('\n', '')
                token_len = len(token)
                state = self.__initial_state
                for i in range(token_len):
                    char = token[i]
                    self.append_char(char)
                    self.create_state(state)
                    
                    next_state = None

                    if i < token_len-1:
                        next_state = self.get_avaible_state(state)
                        self.create_state(next_state)
                    else:
                        next_state = self,get_avaible_state()
                        self.create_state(next_state, True)

        except:
            pass

    def show(self):
        print(self.__fa)
        for state, value in self.__fa.items():
            print(state, '=>', value, '\n')
