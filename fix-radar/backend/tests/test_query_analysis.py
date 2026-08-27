from app.models.enums import QueryCluster, QueryIntent
from app.simulator.query_analysis import extract_entities


def test_executive_query_classifies_as_executive_not_generic_local():
    entities = extract_entities("Who is the best personal trainer for executives in San Diego?")
    assert entities.intent == QueryIntent.EXECUTIVE_HEALTH
    assert entities.cluster == QueryCluster.EXECUTIVE
    assert entities.audience == "executives"
    assert entities.location == "San Diego"


def test_corrective_exercise_query():
    entities = extract_entities("Who specializes in corrective exercise in San Diego?")
    assert entities.intent == QueryIntent.CORRECTIVE_EXERCISE
    assert entities.cluster == QueryCluster.CORRECTIVE_EXERCISE


def test_in_home_query_clusters_as_in_home():
    entities = extract_entities("Who provides premium in-home personal training in La Jolla?")
    assert entities.cluster == QueryCluster.IN_HOME
    assert entities.location == "La Jolla"


def test_age_specific_query():
    entities = extract_entities("Who is a good personal trainer for men over 50 in San Diego?")
    assert entities.cluster == QueryCluster.AGE_SPECIFIC


def test_generic_local_query_falls_back_to_local_cluster():
    entities = extract_entities("What is the best personal trainer in Rancho Santa Fe?")
    assert entities.cluster == QueryCluster.LOCAL
    assert entities.location == "Rancho Santa Fe"
