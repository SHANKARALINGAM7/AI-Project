from collections import defaultdict

def festival_list_to_category_map(festivals):
    """
    Converts FestivalDemand list into:
    { category: [ {festival, date, demand_level}, ... ] }
    """

    category_map = defaultdict(list)

    for f in festivals:
        for category in f.demand_categories:
            category_map[category].append({
                "festival": f.festival_name,
                "date": f.date.strftime("%Y-%m-%d"),
                "demand_level": f.demand_level
            })
    
    
    return dict(category_map)
