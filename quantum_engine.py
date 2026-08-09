import numpy as np
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator

def run_bb84_protocol(num_bits=100, eavesdropper_present=False):
    alice_bits = np.random.randint(2, size=num_bits)
    alice_bases = np.random.randint(2, size=num_bits)
    bob_bases = np.random.randint(2, size=num_bits)
    
    bob_results = []
    simulator = AerSimulator()
    
    for i in range(num_bits):
        qc = QuantumCircuit(1, 1)
        
        # Prepare Alice's qubit
        if alice_bits[i] == 1:
            qc.x(0)
        if alice_bases[i] == 1:
            qc.h(0)
            
        # Interceptor (Eve Attack)
        if eavesdropper_present:
            eve_base = np.random.randint(2)
            if eve_base == 1:
                qc.h(0)
            qc.measure(0, 0)
            if eve_base == 1:
                qc.h(0)
                
        # Bob's measurement
        if bob_bases[i] == 1:
            qc.h(0)
        qc.measure(0, 0)
        
        result = simulator.run(qc, shots=1, memory=True).result()
        measured_bit = int(result.get_memory()[0])
        bob_results.append(measured_bit)
        
    # Key Sifting
    sifted_alice = []
    sifted_bob = []
    
    for i in range(num_bits):
        if alice_bases[i] == bob_bases[i]:
            sifted_alice.append(alice_bits[i])
            sifted_bob.append(bob_results[i])
            
    if not sifted_alice:
        return 0.0, 0, "", "FAILED"
        
    errors = sum(a != b for a, b in zip(sifted_alice, sifted_bob))
    qber = (errors / len(sifted_alice)) * 100
    
    key_str = "".join(map(str, sifted_alice[:16]))
    
    if qber > 11.0:
        return qber, len(sifted_alice), key_str, "ATTACK_DETECTED"
    
    return qber, len(sifted_alice), key_str, "SECURE"
