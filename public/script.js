let serialNo = 1;
let lastDisplayedCount = 0;

async function fetchAccidentData() {
  try {
    const response = await fetch('/data');
    const dataList = await response.json();

    const tableBody = document.querySelector('#accidentTable tbody');

    // Only append rows that haven't been added yet
    const newData = dataList.slice(lastDisplayedCount);
    newData.forEach(data => {
      const row = document.createElement('tr');

      const serialCell = document.createElement('td');
      serialCell.textContent = serialNo++;

      const dateTimeCell = document.createElement('td');
      dateTimeCell.textContent = data.timestamp || new Date().toLocaleString();

      const accidentCell = document.createElement('td');
      let predictionText = data.prediction || "Accident Detected";

      if (data.location && Array.isArray(data.location) && data.location.length === 2) {
        predictionText += ` at (${data.location[0]}, ${data.location[1]})`;
      }

      accidentCell.textContent = predictionText;

      row.appendChild(serialCell);
      row.appendChild(dateTimeCell);
      row.appendChild(accidentCell);

      tableBody.appendChild(row);
    });

    lastDisplayedCount = dataList.length;
  } catch (error) {
    console.error('Error fetching data:', error);
  }
}

// Fetch every 3 seconds
setInterval(fetchAccidentData, 3000);
fetchAccidentData(); // Initial fetch
