import pytest
from pyworkforce.queuing import ErlangC

class TestDefaultErlangCBehaviour:
    """
    Test regular erlangC inputs for single and multi scenario dictionaries.
    """

    
    single_scenario_erlangC_legacy = {"test_scenario 1": {"transactions": 100, "aht": 3.0, "asa": .33, "shrinkage": 0.3, "interval": 30, 'service_level_target':.8}}
    single_scenario_erlangC = {"test_scenario 1": {"transactions": 100, "aht": 3.0, "asa": .33, "shrinkage": 0.3, "interval": 30, 'service_level_target':.8}}
    multiple_scenario_erlangC = {"test_scenario 1": {"transactions": 100, "aht": 3.0, "asa": 20 / 60, "shrinkage": 0.3, "interval": 30, 'service_level_target':.8},
                           "test_scenario 2": {"transactions": [100,200], "aht": 3.0, "asa": 20 / 60, "shrinkage": 0.3, "interval": 30, 'service_level_target':.8}}

    def test_erlangc_single_scenario_results_legacy(self):
        
        erlang = ErlangC(erlang_scenarios=self.single_scenario_erlangC_legacy)
        erlang.calculate_required_positions()
        results = erlang.results_to_dataframe()
        results = results.round(3)
        assert (results['raw_positions'] == 14).all()
        assert (results['positions'] == 19).all()
        assert (results['achieved_service_level'] == 0.888).all()
        assert (results['achieved_occupancy'] == 0.714).all()
        assert (results['waiting_probability'] == 0.174).all()

    def test_erlangc_single_scenario_results(self):
        
        erlang = ErlangC(erlang_scenarios=self.single_scenario_erlangC)
        erlang.calculate_required_positions(enforce_trafficking_requirements=False)
        results = erlang.results_to_dataframe()
        results = results.round(3)

        assert (results['raw_positions'] == 13.1).all()
        assert (results['positions'] == 18.714).all()
        assert (results['achieved_service_level'] == 0.817).all()
        assert (results['achieved_occupancy'] == 0.763).all()
        assert (results['waiting_probability'] == 0.257).all()

    def test_erlangc_multi_scenario_results(self):
        
        erlang = ErlangC(erlang_scenarios=self.multiple_scenario_erlangC)
        erlang.calculate_required_positions(enforce_trafficking_requirements=False)
        results = erlang.results_to_dataframe()
        results = results.round(3)

        columns = ['scenario', 'subscenario', 'transactions', 'aht', 'asa', 'shrinkage',
       'interval', 'service_level_target', 'achieved_service_level',
       'raw_positions', 'positions', 'maximum_occupancy',
       'waiting_probability', 'achieved_occupancy', 'intensity']

        assert results.shape == (3,15)
        assert (results.columns == columns).all()
        assert (results['scenario'].isin(list(self.multiple_scenario_erlangC.keys()) )).all()

        scenario_1 = results[results.scenario == "test_scenario 1"]
        assert (scenario_1['raw_positions'] == 13.1).all()
        assert (scenario_1['positions'] == 18.714).all()
        assert (scenario_1['achieved_service_level'] == 0.818).all()
        assert (scenario_1['achieved_occupancy'] == 0.763).all()
        assert (scenario_1['waiting_probability'] == 0.257).all()

        scenario_2 = results[results.scenario == "test_scenario 2"]
        assert (scenario_2['raw_positions'] == [13.1,23.9]).all()
        assert (scenario_2['positions'] == [18.714, 34.143]).all()
        assert (scenario_2['achieved_service_level'] == [0.818, 0.801]).all()
        assert (scenario_2['achieved_occupancy'] == [0.763, 0.837]).all()
        assert (scenario_2['waiting_probability'] == [0.257, 0.307]).all()
            