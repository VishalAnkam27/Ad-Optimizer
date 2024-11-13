// src/components/PreviousAds.js
import React, { useState, useEffect } from "react";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableRow,
  Button,
  Typography,
  Box,
  CircularProgress,
} from "@mui/material";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import { useCompany } from "../context/CompanyContext"; // Import the company context

const PreviousAds = () => {
  const { companyId } = useCompany(); // Get company ID from the context
  const navigate = useNavigate();
  const [ads, setAds] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // Fetch previous ads when the company ID changes
  useEffect(() => {
    if (companyId) {
      fetchPreviousAds(companyId);
    }
  }, [companyId]);

  const fetchPreviousAds = async (companyId) => {
    setLoading(true);
    setError(null);
    try {
      const response = await axios.get(`/get-optimized-ads/${companyId}`);
      setAds(response.data);
    } catch (err) {
      setError("Failed to fetch previous ads. Please try again.");
      console.error("Error fetching previous ads:", err);
    } finally {
      setLoading(false);
    }
  };

  // Handle navigate to OptimizeAd with the ad's optimized text
  const handleOptimizeAd = (adText, adDetails) => {
    navigate("/optimize-ad", {
      state: { optimizedAdText: adText, ad_details: adDetails },
    });
  };

  return (
    <div style={{ marginTop: "20px" }}>
      <Box
        sx={{
          display: "flex",
          justifyContent: "space-between",
          marginBottom: 2,
        }}
      >
        <Typography variant="h4">Previous Ads</Typography>
        <Button
          variant="contained"
          color="primary"
          size="large"
          onClick={() => navigate("/optimize-ad")}
        >
          Optimize New Ad
        </Button>
      </Box>

      {loading ? (
        <CircularProgress />
      ) : !companyId ? (
        <Typography variant="body1" color="textSecondary">
          Please select a company from the sidebar to view previous ads.
        </Typography>
      ) : error ? (
        <Typography variant="body1" color="error">
          {error}
        </Typography>
      ) : ads.length === 0 ? (
        <Typography variant="body1" color="textSecondary">
          No previous ads available for the selected company.
        </Typography>
      ) : (
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Company</TableCell>
              {/* <TableCell>Property</TableCell> */}
              <TableCell>Original Ad</TableCell>
              <TableCell>Optimized Ad</TableCell>
              <TableCell>Created Date</TableCell>
              <TableCell>Actions</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {ads.map((ad) => (
              <TableRow key={ad.id}>
                <TableCell>
                  {ad?.company_details?.company_name
                    ? ad?.company_details?.company_name
                    : ad?.company_id}
                </TableCell>
                {/* <TableCell>{ad?.property_details?.property_name}</TableCell> */}
                <TableCell>{ad?.original_ad}</TableCell>
                <TableCell>
                  {ad?.selected_ad ? ad?.selected_ad : ad?.optimized_ad}
                </TableCell>
                <TableCell>{ad?.timestamp}</TableCell>
                <TableCell>
                  <Button
                    variant="outlined"
                    onClick={() =>
                      handleOptimizeAd(
                        ad?.selected_ad
                          ? ad?.selected_ad
                          : ad?.optimized_ad?.toString(),
                        ad?.property_details
                      )
                    }
                  >
                    Optimize Ad
                  </Button>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      )}
    </div>
  );
};

export default PreviousAds;
