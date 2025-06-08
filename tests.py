####
# note: all tests were AI generated, because i didnt have time to write all the tests
####
import main as m

def run_tests():
    print("Running Tests:")
    print("-" * 50)
    
    # Temperature tests
    test_cases = [
        ("32F C", "32°F is 0.0°C"),  # Fahrenheit to Celsius
        ("0C F", "0°C is 32.0°F"),  # Celsius to Fahrenheit
        ("273.15K C", "273.15°K is 0.0°C"),  # Kelvin to Celsius
        ("0C K", "0°C is 273.15K"),  # Celsius to Kelvin
        ("491.67R C", "491.67°R is 0.0°C"),  # Rankine to Celsius
        ("0C R", "0°C is 491.67R"),  # Celsius to Rankine
        ("212F K", "212°F is 373.15K"),  # Fahrenheit to Kelvin
        ("100C R", "100°C is 671.67R"),  # Celsius to Rankine
    ]
    
    failed_tests = []
    passed_tests = 0
    
    print("\nTemperature Tests:")
    for test_input, expected in test_cases:
        result = m.convertTemp(test_input.lower().split())
        if result != expected:
            failed_tests.append(("Temperature", test_input, expected, result))
        else:
            passed_tests += 1
    
    # Length tests
    length_tests = [
        # Metric to Metric
        ("1km m", "1km is 1000.0m"),
        ("1m km", "1m is 0.001km"),
        ("100cm m", "100cm is 1.0m"),
        ("1m cm", "1m is 100.0cm"),
        ("1000mm m", "1000mm is 1.0m"),
        ("1m mm", "1m is 1000.0mm"),
        
        # Imperial to Imperial
        ("1ft yd", "1ft is 0.3333333333333333yd"),
        ("1yd ft", "1yd is 3.0ft"),
        ("12in ft", "12in is 1.0ft"),
        ("1ft in", "1ft is 12.0in"),
        ("5280ft mi", "5280ft is 1.0mi"),
        ("1mi ft", "1mi is 5280.0ft"),
        
        # Metric to Imperial
        ("1m ft", "1m is 3.280839895013123ft"),
        ("1ft m", "1ft is 0.3048m"),
        ("1km mi", "1km is 0.621371192237334mi"),
        ("1mi km", "1mi is 1.609344km"),
        
        # Edge cases
        ("0.5km m", "0.5km is 500.0m"),
        ("1.5ft yd", "1.5ft is 0.5yd"),
        ("1000µm m", "1000µm is 0.001m"),
        ("1m µm", "1m is 1000000.0µm"),
    ]
    
    print("\nLength Tests:")
    for test_input, expected in length_tests:
        result = m.convertLength(test_input.split())
        if result != expected:
            failed_tests.append(("Length", test_input, expected, result))
        else:
            passed_tests += 1
    
    weight_tests = [
        # Metric to Metric
        ("1kg g", "1kg is 1000.00g"),
        ("1000g kg", "1000g is 1.00kg"),
        ("1g mg", "1g is 1000.00mg"),
        ("1000mg g", "1000mg is 1.00g"),
        ("1g µg", "1g is 1000000.00µg"),
        ("1000000µg g", "1000000µg is 1.00g"),
        ("1g ng", "1g is 1000000000.00ng"),
        ("1000000000ng g", "1000000000ng is 1.00g"),
        
        # Imperial to Imperial
        ("1lb oz", "1lb is 16.00oz"),
        ("16oz lb", "16oz is 1.00lb"),
        ("1st lb", "1st is 14.00lb"),
        ("14lb st", "14lb is 1.00st"),
        ("1ton lb", "1ton is 2000.00lb"),
        ("2000lb ton", "2000lb is 1.00ton"),
        
        # Metric to Imperial
        ("1kg lb", "1kg is 2.20lb"),
        ("1lb kg", "1lb is 0.45kg"),
        ("1kg oz", "1kg is 35.27oz"),
        ("1oz g", "1oz is 28.35g"),
        ("1tonne ton", "1tonne is 1.10ton"),
        ("1ton tonne", "1ton is 0.91tonne"),
        
        # Edge cases
        ("0.5kg g", "0.5kg is 500.00g"),
        ("1.5lb oz", "1.5lb is 24.00oz"),
        ("0.001g mg", "0.001g is 1.00mg"),
        ("1000µg mg", "1000µg is 1.00mg"),
        ("0.000001g µg", "0.000001g is 1.00µg"),
        ("1.5st lb", "1.5st is 21.00lb"),
        
        # Common reference weights
        ("1tonne kg", "1tonne is 1000.00kg"),
        ("1kg lb", "1kg is 2.20lb"),
        ("1oz g", "1oz is 28.35g"),
        ("1st kg", "1st is 6.35kg"),
    ]
    
    print("\nWeight Tests:")
    for test_input, expected in weight_tests:
        result = m.convertWeight(test_input.split())
        if result != expected:
            failed_tests.append(("Weight", test_input, expected, result))
        else:
            passed_tests += 1
    
    volume_tests = [
        # Metric to Metric
        ("1l ml", "1l is 1000.00ml"),
        ("1000ml l", "1000ml is 1.00l"),
        ("1l cl", "1l is 100.00cl"),
        ("100cl l", "100cl is 1.00l"),
        ("1l dl", "1l is 10.00dl"),
        ("10dl l", "10dl is 1.00l"),
        ("1l kl", "1l is 0.00kl"),
        ("1kl l", "1kl is 1000.00l"),
        ("1l µl", "1l is 1000000.00µl"),
        ("1000000µl l", "1000000µl is 1.00l"),
        
        # Imperial to Imperial
        ("1gal qt", "1gal is 4.00qt"),
        ("4qt gal", "4qt is 1.00gal"),
        ("1qt pt", "1qt is 2.00pt"),
        ("2pt qt", "2pt is 1.00qt"),
        ("1pt floz", "1pt is 16.00floz"),
        ("16floz pt", "16floz is 1.00pt"),
        ("1cup floz", "1cup is 8.00floz"),
        ("8floz cup", "8floz is 1.00cup"),
        ("1tbsp tsp", "1tbsp is 3.00tsp"),
        ("3tsp tbsp", "3tsp is 1.00tbsp"),
        
        # Cubic measurements
        ("1ft3 in3", "1ft3 is 1728.00in3"),
        ("1728in3 ft3", "1728in3 is 1.00ft3"),
        ("1yd3 ft3", "1yd3 is 27.00ft3"),
        ("27ft3 yd3", "27ft3 is 1.00yd3"),
        
        # Metric to Imperial
        ("1l gal", "1l is 0.26gal"),
        ("1gal l", "1gal is 3.79l"),
        ("1l floz", "1l is 33.81floz"),
        ("1floz ml", "1floz is 29.57ml"),
        ("1ft3 l", "1ft3 is 28.32l"),
        ("1l ft3", "1l is 0.04ft3"),
        
        # Edge cases
        ("0.5l ml", "0.5l is 500.00ml"),
        ("1.5gal qt", "1.5gal is 6.00qt"),
        ("0.001l ml", "0.001l is 1.00ml"),
        ("1000µl ml", "1000µl is 1.00ml"),
        ("0.000001l µl", "0.000001l is 1.00µl"),
        ("1.5qt pt", "1.5qt is 3.00pt"),
        
        # Common reference volumes
        ("1gal l", "1gal is 3.79l"),
        ("1l gal", "1l is 0.26gal"),
        ("1cup ml", "1cup is 236.59ml"),
        ("1tbsp ml", "1tbsp is 14.79ml"),
    ]
    
    print("\nVolume Tests:")
    for test_input, expected in volume_tests:
        result = m.convertVolume(test_input.split())
        if result != expected:
            failed_tests.append(("Volume", test_input, expected, result))
        else:
            passed_tests += 1
    
    # Print summary
    total_tests = len(test_cases) + len(length_tests) + len(weight_tests) + len(volume_tests)
    print("\nTest Summary:")
    print(f"Passed: {passed_tests}/{total_tests}")
    print(f"Failed: {len(failed_tests)}/{total_tests}")
    
    if failed_tests:
        print("\nFailed Tests:")
        print("-" * 50)
        for test_type, test_input, expected, result in failed_tests:
            print(f"Type: {test_type}")
            print(f"Input: {test_input}")
            print(f"Expected: {expected}")
            print(f"Got: {result}")
            print("-" * 50)

if __name__ == "__main__":
    run_tests()