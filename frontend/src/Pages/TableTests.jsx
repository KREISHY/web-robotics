import React, { useState } from "react";
import 'bootstrap/dist/css/bootstrap.min.css';
import axiosConfig from "./Components/AxiosConfig";

function TableTests({ nameTeam }) {
  const [test, setTest] = useState(2);
  const [rows, setRows] = useState(
    Array.from({ length: test }, () => ({
      accuracy: '',
      speed: '',
      creativity: '',
    }))
  );

  const checkNum = (value) => {
    return value.replace(/[^0-9]/g, '');
  };

  const handleInputChange = (index, field, value) => {
    const newRows = [...rows];
    newRows[index][field] = checkNum(value);
    setRows(newRows);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axiosConfig.post("/api/submit-data/", {
        teamName: nameTeam,
        tests: rows,
      });
      if (response.status === 200) {
        console.log('Данные успешно отправлены');
      } else {
        console.error('Ошибка при отправке данных');
      }
    } catch (error) {
      console.error('Ошибка при отправке данных: ', error);
    }
  };

  return (
    <div className="container mt-5">
      <h2 className="text-center mb-4" style={{ fontWeight: 'bold' }}>{nameTeam}</h2>
      <div className="table-responsive">
        <form onSubmit={handleSubmit}>
          <table className="table table-bordered table-hover">
            <thead className="thead-light">
              <tr>
                <th></th>
                <th style={{ fontWeight: 'bold', textAlign: 'center' }}>Точность</th>
                <th style={{ fontWeight: 'bold', textAlign: 'center' }}>Скорость</th>
                <th style={{ fontWeight: 'bold', textAlign: 'center' }}>Креативность</th>
              </tr>
            </thead>
            <tbody>
              {Array.from({ length: test }).map((_, i) => (
                <tr key={i}>
                  <td style={{ fontWeight: 'bold', textAlign: 'center' }}>Испытание {i + 1}</td>
                  <td style={{ textAlign: 'center' }}>
                    <input
                      type="text"
                      className="form-control"
                      value={rows[i].accuracy}
                      onChange={(e) => handleInputChange(i, 'accuracy', e.target.value)}
                    />
                  </td>
                  <td style={{ textAlign: 'center' }}>
                    <input
                      type="text"
                      className="form-control"
                      value={rows[i].speed}
                      onChange={(e) => handleInputChange(i, 'speed', e.target.value)}
                    />
                  </td>
                  <td style={{ textAlign: 'center' }}>
                    <input
                      type="text"
                      className="form-control"
                      value={rows[i].creativity}
                      onChange={(e) => handleInputChange(i, 'creativity', e.target.value)}
                    />
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
          <div className="text-center mt-3">
            <button type="submit" className="btn btn-primary">Отправить</button>
          </div>
        </form>
      </div>
    </div>
  );
}

export default TableTests;