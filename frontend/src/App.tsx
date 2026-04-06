import React, { useEffect, useState } from "react";
import "./index.css";
import Search from "./comps/Search";
import HeaderBar from "./comps/HeaderBar";
import { ThemeProvider } from "./components/ui/theme-provider";
import Map from "./comps/Map";
import Content from "./comps/Content";

const App = () => {

  const [data, setData] = useState([]);
  const [cities, setCities] = useState([])

  useEffect(() => {
  fetch("http://127.0.0.1:8000/data")
    .then(res => res.json())
    .then(data => setData(data));
}, []);

  const uniqueCities = [...new Set(data.map((item) => item.city))];

  

  return (
    <ThemeProvider>
      <div className="flex justify-center flex-col items-center">
        <HeaderBar />
        <Search set_city={setCities} cities_data={uniqueCities} />
        <div className="bg-red-500 w-full h-130 flex flex-row place-items-center place-content-between " >
          <Content />
          <Map />
        </div>
      </div>
    </ThemeProvider>
  );
};

export default App;
