import unittest
from plot import Graph
import pandas as pd
import numpy as np

class TestHosinoPlot(unittest.TestCase):
    def setUp(self):
        # Create a mock DataFrame for testing
        data = {
            '측정일': pd.date_range(start='2022-01-01', end='2022-01-31', freq='D'),
            '침하량': np.random.randint(10, 50, size=31)
        }
        df = pd.DataFrame(data)

        # Create a Graph object
        self.graph = Graph(df, '2022-01-01', '2022-01-15', 15)

    def test_hosino_plot_different_lengths(self):
        # Create a mock date_pred with a different length
        date_pred = pd.date_range(start='2022-01-01', end='2022-01-20', freq='D')
        self.graph.date_pred = date_pred

        # Call the hosino_plot method
        result = self.graph.hosino_plot()

        # Verify the lengths of the combined_dates, s_pred_combined, and raw_settlement_combined
        self.assertEqual(len(result[0]), len(result[1]), len(result[2]))

if __name__ == '__main__':
    unittest.main()