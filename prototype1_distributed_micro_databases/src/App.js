import './App.css';
import QueryReader from './pages/QueryReader';
import {
  BrowserRouter as Router,
  Route
} from "react-router-dom";
import QueryResult from './pages/QueryResult';

function App() {
  return (
      <div className="App">
        <Route path='/' exact component={QueryReader} />
        <Route path='/queryResult' exact component={QueryResult} />
      </div>
  );
}

export default App;
