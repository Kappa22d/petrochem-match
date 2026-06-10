"""Engineering tools and calculators blueprint."""
from flask import Blueprint, render_template, request, jsonify
from app.models import Chemical

tools_bp = Blueprint('tools', __name__)


@tools_bp.route('/esg-calculator')
def esg_calculator():
    return render_template('tools/esg_calculator.html')


@tools_bp.route('/esg-calculator/calculate', methods=['POST'])
def calculate_esg():
    data = request.get_json()
    
    annual_usage_kg = float(data.get('annual_usage_kg', 0))
    old_emissions = float(data.get('old_emissions_factor', 0))
    new_emissions = float(data.get('new_emissions_factor', 0))
    
    old_total_emissions = annual_usage_kg * old_emissions
    new_total_emissions = annual_usage_kg * new_emissions
    emissions_reduction = old_total_emissions - new_total_emissions
    reduction_percentage = (emissions_reduction / old_total_emissions * 100) if old_total_emissions > 0 else 0
    
    co2_offset_trees = emissions_reduction / 21
    
    return jsonify({
        'old_total_emissions': round(old_total_emissions, 2),
        'new_total_emissions': round(new_total_emissions, 2),
        'emissions_reduction': round(emissions_reduction, 2),
        'reduction_percentage': round(reduction_percentage, 1),
        'co2_offset_trees': round(co2_offset_trees, 0),
    })


@tools_bp.route('/chemical-lookup')
def chemical_lookup():
    return render_template('tools/chemical_lookup.html')


@tools_bp.route('/chemical-lookup/search', methods=['GET'])
def search_chemical():
    query = request.args.get('q', '')
    
    results = Chemical.query.filter(
        (Chemical.name.ilike(f'%{query}%')) |
        (Chemical.cas_number.ilike(f'%{query}%'))
    ).limit(10).all()
    
    return jsonify({
        'results': [r.to_dict() for r in results]
    })


@tools_bp.route('/unit-converter')
def unit_converter():
    return render_template('tools/unit_converter.html')


@tools_bp.route('/unit-converter/convert', methods=['POST'])
def convert_units():
    data = request.get_json()
    value = float(data.get('value', 0))
    from_unit = data.get('from_unit', '')
    to_unit = data.get('to_unit', '')
    
    conversions = {
        ('kg', 'lbs'): value * 2.20462,
        ('lbs', 'kg'): value / 2.20462,
        ('m3', 'bbl'): value * 6.28981,
        ('bbl', 'm3'): value / 6.28981,
        ('celsius', 'fahrenheit'): (value * 9/5) + 32,
        ('fahrenheit', 'celsius'): (value - 32) * 5/9,
        ('atm', 'psi'): value * 14.6959,
        ('psi', 'atm'): value / 14.6959,
    }
    
    key = (from_unit, to_unit)
    result = conversions.get(key, None)
    
    if result is None:
        return jsonify({'error': 'Conversion not supported'}), 400
    
    return jsonify({'result': round(result, 4), 'value': value, 'from': from_unit, 'to': to_unit})
