import React, { useState, useEffect } from "react";
import { fetchPreviousAds } from "../services/api";

const TableView = ({ selectedCompany, selectedProperty, setCurrentView }) => {
  const [ads, setAds] = useState([]);

  useEffect(() => {
    if (selectedCompany && selectedProperty) {
      fetchPreviousAds(selectedCompany, selectedProperty).then(setAds);
    }
  }, [selectedCompany, selectedProperty]);

  return (
    <div className="table-view">
      <h2>Previous Ads</h2>
      {ads.length > 0 ? (
        <table>
          <thead>
            <tr>
              <th>Ad Text</th>
              <th>Date</th>
              <th>Action</th>
            </tr>
          </thead>
          <tbody>
            {ads.map((ad, index) => (
              <tr key={index}>
                <td>{ad.ad_text}</td>
                <td>{ad.date}</td>
                <td>
                  <button onClick={() => setCurrentView("optimize")}>
                    Optimize Ad
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      ) : (
        <p>No previous ads available for this selection.</p>
      )}
    </div>
  );
};

export default TableView;
