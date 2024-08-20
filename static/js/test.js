const baseurl = 'http://127.0.0.1:8000/';
const dymanicurl = 'fetchdata/api/fetchdata';
const url = baseurl + dymanicurl;
console.log(url);
let count = 0;

async function fetchData(conditionName) {
  try {
    const response = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ conditionName: conditionName })
    });
    if (!response.ok) {
      throw new Error('Failed to fetch data');
    }
    const data = await response.json();
    console.log(data);
    return data;
  } catch (error) {
    console.error(error);
  }
}

function generateStockTable(data, tableId, modelName, tableName) {
  const tableContainer = document.getElementById(tableId);
  tableContainer.innerHTML = ''; // Clear existing table content
  const groupedData = {};
  data.forEach(item => {
    const { sector, nsecode, frequency, close, per_chg, count } = item;
    if (sector && nsecode) {
      if (!groupedData[sector]) {
        groupedData[sector] = [];
      }
      groupedData[sector].push({ nsecode, frequency, close, per_chg, count });
    }
  });

  const sectors = Object.keys(groupedData).map(sector => {
    const companies = groupedData[sector];
    return {
      sector,
      companies,
      totalFrequency: companies.reduce((acc, curr) => acc + curr.frequency, 0),
      highestPerChg: Math.max(...companies.map(c => c.per_chg))
    };
  });

  sectors.sort((a, b) => {
    if (b.totalFrequency === a.totalFrequency) {
      return b.highestPerChg - a.highestPerChg;
    }
    return b.totalFrequency - a.totalFrequency;
  });

  const table = document.createElement('table');
  table.classList.add('table', 'table-bordered');

  const thead = document.createElement('thead');
  const headerRow = document.createElement('tr');
  const headers = ['SECTOR', 'CLOSE', '% CHANGE', 'COUNT'];
  headers.forEach(headerText => {
    const th = document.createElement('th');
    th.textContent = headerText;
    th.classList.add('custom-header');
    headerRow.appendChild(th);
  });
  thead.appendChild(headerRow);
  table.appendChild(thead);

  const tbody = document.createElement('tbody');

  sectors.forEach(({ sector, companies }) => {
    const sectorRow = document.createElement('tr');
    sectorRow.classList.add('sector-header');
    
    const sectorCell = document.createElement('td');
    const totalCompanies = companies.length;
    sectorCell.colSpan = headers.length;
    sectorCell.textContent = `${sector} - (${totalCompanies})`;
    sectorRow.appendChild(sectorCell);

    tbody.appendChild(sectorRow);

    companies.sort((a, b) => b.per_chg - a.per_chg);

    companies.forEach(company => {
      const companyRow = document.createElement('tr');
      companyRow.classList.add('company-row');
      
      const companyCells = ['nsecode', 'close', 'per_chg', 'count'];
      companyCells.forEach(cellType => {
        const companyCell = document.createElement('td');
        if (cellType === 'nsecode') {
          
          const link = document.createElement('a');
          link.href = `https://www.tradingview.com/chart/?symbol=NSE%3A${company[cellType]}`;
          link.textContent = company[cellType];
          link.target = '_blank';
          companyCell.style.textAlign = 'left';
          companyCell.appendChild(link);
        } else if (cellType === 'per_chg') {
          const value = company[cellType];
          companyCell.textContent = `${value}%`;
          if (value > 0) {
            companyCell.style.backgroundColor = '#c6f0c6';
          } else if (value < 0) {
            companyCell.style.backgroundColor = '#f8d7da';
          }
        } else if (cellType === 'count') {
          const countValue = company[cellType];
          companyCell.textContent = countValue;
          companyCell.style.color = 'black'; // Ensure count value text color is black
          // Set background color based on count value
          if (countValue === 1) {
            companyCell.style.backgroundColor = 'yellow'; // Yellow for count = 1
            companyCell.style.color = 'black'; // Ensure count value text color is black
          } else if (countValue > 1) {
            companyCell.style.backgroundColor = 'green'; // Green for count > 1
            companyCell.style.color = 'white'; // Ensure count value text color is black
          }
          companyCell.classList.add('count-cell');
          companyCell.setAttribute('data-company', JSON.stringify(company));
          companyCell.onclick = () => showPopup(company, tableName, sector, modelName);
        } else {
          companyCell.textContent = company[cellType];
        }
        companyCell.style.textAlign = 'center'; // Center align text
        companyRow.appendChild(companyCell);
      });

      tbody.appendChild(companyRow);
    });
  });

  table.appendChild(tbody);
  tableContainer.appendChild(table);
}

async function getCount(modelName, nsecode, count) {
  const fetchUrl = 'fetchdata/api/fetchfrequency';
  const newUrl = baseurl + fetchUrl;
  const response = await fetch(newUrl, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ tableName: modelName, nsecode: nsecode, count: count })
  });
  if (!response.ok) {
    throw new Error('Failed to fetch data');
  }
  const data = await response.json();
  console.log('Success:', data);
  return data;
}

async function showPopup(company, tableName, sector, modelName) {
  const popupOverlay = document.getElementById('popup-overlay');
  const popupContent = document.getElementById('popup-content');

  try {
    const response = await getCount(modelName, company.nsecode, company.count);
    const freqData = response.data; // Access the data from the response
    
    // Create a table for the list data
    let listTableHtml = '<table class="table table-bordered popup-table mt-3"><thead><tr>';
    
    // Check if freqData is an array and contains data
    if (Array.isArray(freqData) && freqData.length > 0) {
      const columns = Object.keys(freqData[0]); // Get the columns from the first item
      columns.forEach(column => {
        listTableHtml += `<th>${column.toUpperCase()}</th>`;
      });
      listTableHtml += '</tr></thead><tbody>';
      
      freqData.forEach(item => {
        listTableHtml += '<tr>';
        columns.forEach(column => {
          listTableHtml += `<td>${item[column]}</td>`;
        });
        listTableHtml += '</tr>';
      });
      
      listTableHtml += '</tbody></table>';
    } else {
      listTableHtml = '<p>No data available.</p>';
    }

    popupContent.innerHTML = `
      <h4 id="popup-title">In - ${tableName}</h4>
      <h3>${company.nsecode}</h3>
      <p>Sector: ${sector}</p>
      <p>Price: ${company.close}</p>
      <p>Percentage Change: ${company.per_chg}%</p>
      <p>Appearance in Last 30 days: ${company.count} times</p>
      <canvas id="close-chart" width="400" height="200"></canvas>
      ${listTableHtml}
    `;
    
    const popup = document.querySelector('.popup');
    popup.style.display = 'block';
    popupOverlay.style.display = 'flex';

    freqData.sort((a, b) => {
      // Convert date strings to Date objects
      let dateA = new Date(a.date.split('-').reverse().join('-'));
      let dateB = new Date(b.date.split('-').reverse().join('-'));

      // Compare the Date objects
      return dateA - dateB;
    });

    // Generate chart
    const closeChart = document.getElementById('close-chart').getContext('2d');
    const labels = freqData.map(item => {
      const [day, month] = item.date.split('-');
      return `${day}-${month}`;
    });
    const closeValues = freqData.map(item => item.close);
    
    new Chart(closeChart, {
      type: 'line',
      data: {
        labels: labels,
        datasets: [{
          label: 'Close',
          data: closeValues,
          borderColor: 'rgba(54, 162, 235, 1)', // Blue color for line
          backgroundColor: 'rgba(54, 162, 235, 0.2)', // Light blue color for the fill
          borderWidth: 2,
          fill: true,
          tension: 0.1
        }]
      },
      options: {
        responsive: true,
        plugins: {
          legend: {
            labels: {
              color: '#333'
            }
          }
        },
        scales: {
          x: {
            display: true,
            title: {
              display: true,
              text: 'Date',
              color: '#333'
            },
            grid: {
              color: '#ddd'
            }
          },
          y: {
            display: true,
            title: {
              display: true,
              text: 'Close Value',
              color: '#333'
            },
            grid: {
              color: '#ddd'
            }
          }
        }
      }
    });
  } catch (error) {
    console.error('Error fetching frequency data:', error);
  }
}

function closePopup() {
  const popupOverlay = document.getElementById('popup-overlay');
  popupOverlay.style.display = 'none';
}

async function fetchDataWithDelay(conditionName, tableId, delay, modelName, tableName) {
  await new Promise(resolve => setTimeout(resolve, delay));
  const data = await fetchData(conditionName);
  if (data) {
    generateStockTable(data, tableId, modelName, tableName);
  }
}

async function init() {
  await fetchDataWithDelay('Champions Intraday', 'intraday-table', 50, 'IntradayData', 'INTRADAY');
  await fetchDataWithDelay('Champions Over Brought', 'overbrought-table', 50, 'OverBroughtData', 'OVERBOUGHT');
  await fetchDataWithDelay('Champions Positional', 'positional-table', 50, 'PositionalData', 'POSITIONAL');
  await fetchDataWithDelay('Champions Swing', 'swing-table', 50, 'SwingData', 'SWING');
  await fetchDataWithDelay('Champions Reversal Stocks', 'reversal-table', 50, 'ReversalData', 'REVERSAL');
  count++;
  console.log(`------Count: ${count}-----`);
}

init();
setInterval(init, 20000); // Refresh every 20 seconds
