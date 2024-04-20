import graphviz

class DFA:
    def __init__(self, states, alphabet, transitions, start_state, accept_states):
        self.states = states
        self.alphabet = alphabet
        self.transitions = transitions
        self.start_state = start_state
        self.accept_states = accept_states

    def is_accepting(self, state):
        return state in self.accept_states

    def transition(self, state, symbol):
        if (state, symbol) in self.transitions:
            return self.transitions[(state, symbol)]
        else:
            return None

    def minimize(self):
        from collections import defaultdict

        partition = [self.accept_states, self.states - self.accept_states]
        changed = True
        while changed:
            changed = False
            new_partition = []
            for part in partition:
                split_dict = defaultdict(list)
                for state in part:
                    transition_key = tuple(self.transition(state, symbol) for symbol in self.alphabet)
                    split_dict[transition_key].append(state)
                if len(split_dict) > 1:
                    changed = True
                    new_partition.extend(split_dict.values())
                else:
                    new_partition.append(part)
            partition = new_partition

        state_map = {}
        minimized_states = set()
        minimized_accept_states = set()
        minimized_transitions = {}

        for part in partition:
            representative = next(iter(part))
            minimized_states.add(representative)
            if representative in self.accept_states:
                minimized_accept_states.add(representative)
            for state in part:
                state_map[state] = representative

        for (state, symbol), next_state in self.transitions.items():
            new_state = state_map[state]
            new_next_state = state_map[next_state]
            minimized_transitions[(new_state, symbol)] = new_next_state

        self.states = minimized_states
        self.transitions = minimized_transitions
        self.accept_states = minimized_accept_states
        self.start_state = state_map[self.start_state]


    def simulate(self, input_string):
        current_state = self.start_state

        for symbol in input_string:
            current_state = self.transition(current_state, symbol)
            if current_state is None:
                return False
        
        return self.is_accepting(current_state)
    def __str__(self):
        return f"States: {self.states}\nAlphabet: {self.alphabet}\nTransitions: {self.transitions}\nStart State: {self.start_state}\nAccept States: {self.accept_states}"


def get_dfa_from_user():
    states = input("Masukkan states (pisahkan dengan koma): ").split(',')
    alphabet = input("Masukkan alphabet (pisahkan dengan koma): ").split(',')
    start_state = input("Masukkan start state: ")
    accept_states = input("Masukkan accept states (pisahkan dengan koma): ").split(',')

    transitions = {}
    print("Masukkan transitions (format: state, symbol, next_state). Ketik 'selesai' untuk berhenti.")
    while True:
        transition_input = input("Transition: ")
        if transition_input.lower() == 'selesai':
            break
        state, symbol, next_state = transition_input.split(',')
        transitions[(state.strip(), symbol.strip())] = next_state.strip()

    return DFA(set(states), set(alphabet), transitions, start_state, set(accept_states))

def visualize_automaton(states, alphabet, transitions, start_state, accept_states, name):
    # Membuat digraph objek
    dot = graphviz.Digraph()
    
    dot.attr(rankdir='LR')
    dot.attr('node', shape='circle')
    
    # Menambah node
    for state in states:
        if state in accept_states:
            dot.node(state, shape='doublecircle')
        else:
            dot.node(state)
    
    # Menambah start node
    dot.node('start', shape='point')
    dot.edge('start', start_state)
    
    # Tambah transisi
    for transition in transitions:
        from_state, symbol = transition
        to_state = transitions[transition]
        dot.edge(from_state, to_state, label=symbol)
    
    # Merender
    dot.render(name, format='png', view=True)

def main():
    dfa = get_dfa_from_user()
    input_string = input("\nMasukkan string untuk diuji: ")

    print("\nDFA sebelum minimasi:")
    print("Hasil pengujian:", "Diterima" if dfa.simulate(input_string) else "Ditolak")
    print(dfa)
    visualize_automaton(dfa.states, dfa.alphabet, dfa.transitions, dfa.start_state, dfa.accept_states, 'dfa1')

    dfa.minimize()  # Panggil fungsi minimize di sini

    print("\nDFA setelah minimasi:")
    print("Hasil pengujian:", "Diterima" if dfa.simulate(input_string) else "Ditolak")
    visualize_automaton(dfa.states, dfa.alphabet, dfa.transitions, dfa.start_state, dfa.accept_states, 'dfa2')

if __name__ == "__main__":
    main()
