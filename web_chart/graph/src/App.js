import { useEffect, useState } from 'react';
import axios from 'axios';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';


export default function App() {
  const [prices, setPrices] = useState([]);
  useEffect(() => {
    const arr = [];
    /*axios(url, {
      headers: {
        "Access-Control-Allow-Origin": "*",
      }
    })
    .then(response => {for(let x=0;x < response.data.length;x++){arr.push(response.data[x])}})
    setStockData(arr)*/


    const getData = async () => {  
      await axios.get(`http://localhost:5000/`, {
        headers: {
          "Access-Control-Allow-Origin": "*",
        }
      })  
      .then((res) => {  
        //const data = JSON.parse(res.data);
        if(typeof(res.data) !== "undefined"){
          if(res.data.length > prices.length){
            const price = res.data;
            checkPrices(price);
          }
        };
      })
      .catch(err => {  
        console.log(err)  
      });  
    }  
    getData()

  }, []);
  function checkPrices(price){
    console.log('price',price)
    console.log('prices', prices);
    const arr = [];
    if(price.length !== prices.length){
      for(let i=0;i<price.length;i++){
        const dec = parseFloat(price[i]['price'][0])
        prices.push({'price': dec})
        const p = {'price': dec};
      }
      setPrices(prev => [...prev,prices]);
      console.log(prices[0]['price']);
      console.log(prices)
    }
  }
  return (
    <div style={{ width: '50vw', height: '50vh'}}>
      <ResponsiveContainer width="100%" height="100%">
        <LineChart
          width={500}
          height={300}
          data={prices}
          margin={{
            top: 5,
            right: 30,
            left: 20,
            bottom: 5,
          }}
        >
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis />
          <YAxis type="number" domain={['dataMin', 'dataMax']} />
          <Tooltip />
          <Legend />
          <Line type="monotone" dataKey="price" stroke="#8884d8" activeDot={{ r: 8 }} />
        </LineChart>
      </ResponsiveContainer>
    </div>
  )
}