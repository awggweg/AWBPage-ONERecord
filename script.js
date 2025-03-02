
document.addEventListener('DOMContentLoaded', function() {
    document.querySelector('.submit-btn').addEventListener('click', processInput);
  });
  document.querySelector('.submit-btn').addEventListener('click', function() {
    var userInput = document.getElementById('user-input').value;
    
    getShipperName(userInput);
  });
  function getShipperName(userInput) {
    const sparql = `
      PREFIX cargo: <https://onerecord.iata.org/ns/cargo#>
      PREFIX code: <https://onerecord.iata.org/ns/code-lists/>
      SELECT ?name WHERE {
        ?party a cargo:Party ;
               cargo:partyRole <https://onerecord.iata.org/ns/code-lists/ParticipantIdentifier#SHP> ;
               cargo:partyDetails [ cargo:name ?name ] .
      }`;
    callApi(userInput, sparql).then(data => {
      // 提取第一个结果的 name 字段
      const name = data.results[0].name;
      // 显示到前端（假设有一个 id 为 "result" 的 HTML 元素）
      document.getElementById("result").textContent = name;
    }).catch(error => {
      console.error("Error fetching data:", error);
    });
  }
function processInput() {
    var userInput = document.getElementById('user-input').value;
    console.log("User hello input:", userInput);
}

function callApi(userInput,sparql) {

  var data = {
    sparql: sparql,
    jsonld: JSON.parse(userInput)
  };


  return fetch('http://localhost:5000/query', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(data)
  })
  .then(response => response.json())
  .then(data => {
    console.log('Success:', data);
    // You can handle the response data here
    return data;
  })
  .catch((error) => {
    console.error('Error:', error);
  });
}

