from flask import Flask, request, jsonify
from itertools import permutations
from collections import defaultdict
import math

app = Flask(__name__)

# Product information mapping
product_info = {
    'A': {'center': 'C1', 'weight': 3},
    'B': {'center': 'C1', 'weight': 2},
    'C': {'center': 'C1', 'weight': 8},
    'D': {'center': 'C2', 'weight': 12},
    'E': {'center': 'C2', 'weight': 25},
    'F': {'center': 'C2', 'weight': 15},
    'G': {'center': 'C3', 'weight': 0.5},
    'H': {'center': 'C3', 'weight': 1},
    'I': {'center': 'C3', 'weight': 2},
}

# Corrected distance matrix (units)
distance_matrix = {
    ('C1', 'C2'): 4,
    ('C1', 'L1'): 3,
    ('C2', 'L1'): 3,
    ('C3', 'L1'): 2,
    ('C2', 'C1'): 4,
    ('L1', 'C1'): 3,
    ('L1', 'C2'): 3,
    ('L1', 'C3'): 2,
    ('C1', 'C3'): 5,  # C1 -> L1 -> C3
    ('C3', 'C1'): 5,
    ('C2', 'C3'): 5,  # C2 -> L1 -> C3
    ('C3', 'C2'): 5,
}

def get_distance(from_loc, to_loc):
    return distance_matrix.get((from_loc, to_loc), 0)

def calculate_cost_per_unit(weight):
    if weight <= 5:
        return 10
    excess = weight - 5
    increments = math.ceil(excess / 5)
    return 10 + 8 * increments

def compute_min_cost(order):
    required_centers = defaultdict(float)
    for product, qty in order.items():
        info = product_info.get(product)
        if not info or qty <= 0:
            continue
        center = info['center']
        weight = info['weight'] * qty
        required_centers[center] += weight

    if not required_centers:
        return 0

    min_total_cost = float('inf')

    for deployment in ['C1', 'C2', 'C3']:
        deployment_has_products = deployment in required_centers
        deployment_weight = required_centers.get(deployment, 0.0)
        other_centers = [center for center in required_centers if center != deployment]
        centers_for_perm = other_centers

        perms = list(permutations(centers_for_perm)) if centers_for_perm else [()]
        for perm in perms:
            n = len(perm)
            # Fix: Use n bits instead of n-1 to allow L1 insertion after deployment
            for mask in range(0, 1 << n):
                route = [deployment]
                current_weight = deployment_weight if deployment_has_products else 0.0

                # Check if L1 should be inserted immediately after deployment
                if (mask >> 0) & 1 and n >= 1:
                    route.append('L1')
                    current_weight = 0.0

                for i in range(n):
                    center = perm[i]
                    route.append(center)
                    if (mask >> (i + 1)) & 1 and i < n - 1:
                        route.append('L1')
                        current_weight = 0.0
                route.append('L1')

                total_cost = 0.0
                current_location = deployment
                current_weight_leg = deployment_weight if deployment_has_products else 0.0

                for step in route[1:]:
                    if step == 'L1':
                        distance = get_distance(current_location, 'L1')
                        cost_per = calculate_cost_per_unit(current_weight_leg)
                        total_cost += distance * cost_per
                        current_weight_leg = 0.0
                        current_location = 'L1'
                    else:
                        distance = get_distance(current_location, step)
                        cost_per = calculate_cost_per_unit(current_weight_leg)
                        total_cost += distance * cost_per
                        current_weight_leg += required_centers[step]
                        current_location = step

                if total_cost < min_total_cost:
                    min_total_cost = total_cost

    return min_total_cost

@app.route('/calculate-cost', methods=['POST'])
def calculate_cost_endpoint():
    order = request.get_json()
    if not order:
        return jsonify({'error': 'Invalid input'}), 400
    min_cost = compute_min_cost(order)
    return jsonify({'min_cost': min_cost})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)