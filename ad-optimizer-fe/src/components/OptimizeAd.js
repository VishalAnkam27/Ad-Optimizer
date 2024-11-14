// src/components/OptimizeAd.js
import React, { useState, useEffect } from "react";
import {
  Box,
  Typography,
  TextField,
  Button,
  Card,
  CardContent,
  CircularProgress,
  Skeleton,
  Divider,
  Grid,
  Radio,
  RadioGroup,
  FormControlLabel,
  FormControl,
} from "@mui/material";
import { useDropzone } from "react-dropzone"; // For image upload
import axios from "axios";
import { useCompany } from "../context/CompanyContext";
import { useNavigate, useLocation } from "react-router-dom"; // For navigation state
import { motion } from "framer-motion"; // For animations

const OptimizeAd = () => {
  const { companyId, propertyId } = useCompany();
  const navigate = useNavigate();
  const location = useLocation();
  const [inputType, setInputType] = useState("text"); // State to track the selected input type
  const [adText, setAdText] = useState(location.state?.optimizedAdText || ""); // Prefill text if passed
  const [image, setImage] = useState(null); // State to store the image file
  const [adDetails, setAdDetails] = useState(location.state?.ad_details || ""); // State to store the ad details
  const [optimizedAds, setOptimizedAds] = useState([]); // State to store optimized ads
  const [selectedAdIndex, setSelectedAdIndex] = useState(null); // State to track selected ad
  const [sampleAd, setSampleAd] = useState(
    "Boost your property visibility with our new beachfront luxury homes campaign!"
  ); // Default sample ad
  const [sampleAdDetails, setSampleAdDetails] = useState(
    "Targeted towards high-net-worth individuals interested in beachfront properties."
  );
  const [loadingSample, setLoadingSample] = useState(false);
  const [loading, setLoading] = useState(false); // State to track loading status
  const [error, setError] = useState(null); // State to track errors
  const [optimizationId, setOptimizationId] = useState(null);
  useEffect(() => {
    if (companyId) {
      fetchSampleAd(companyId);
    }
  }, [companyId]);

  const fetchSampleAd = async (companyId) => {
    setLoadingSample(true);
    setError(null);
    try {
      const response = await axios.get(`/get-sample-ad/${companyId}`);
      setSampleAd(response.data.sample_ad || sampleAd);
      setSampleAdDetails(response.data.sample_ad_details || sampleAdDetails);
    } catch (err) {
      console.error("Error fetching sample ad:", err);
    } finally {
      setLoadingSample(false);
    }
  };

  const handleTextChange = (e) => {
    setAdText(e.target.value);
  };

  const handleAdDetailsChange = (e) => {
    setAdDetails(e.target.value);
  };

  const onDrop = (acceptedFiles) => {
    setImage(acceptedFiles[0]);
  };
  const { getRootProps, getInputProps } = useDropzone({
    onDrop,
    accept: "image/*",
  });

  const handleOptimizeAd = async () => {
    if (inputType === "text" && !adText) {
      setError("Please enter ad text.");
      return;
    }

    if (!companyId) {
      setError("Please provide a company ID.");
      return;
    }

    setLoading(true);
    setError(null);

    try {
      // Create FormData for handling both image and text
      const formData = new FormData();
      formData.append("company_id", companyId);
      if (propertyId) {
        formData.append("property_id", propertyId);
      }
      formData.append("ad_details", JSON.stringify(adDetails));

      // Attach image if inputType is 'image', otherwise attach the ad text
      if (inputType === "image" && image) {
        formData.append("ad_image", image);
      } else {
        formData.append("ad_text", adText);
      }
      console.log("🚀 ~ handleOptimizeAd ~ formData:", formData);

      const response = await axios.post("/optimize-ad", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });
      setOptimizationId(response?.data?.optimized_ads?.optimization_id);
      setOptimizedAds(response?.data?.optimized_ads?.optimized_ads || []);
      setSelectedAdIndex(null); // Reset selected ad index
    } catch (err) {
      setError("Failed to optimize ad: " + err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleUseSampleAd = () => {
    setAdText(sampleAd);
    setAdDetails(sampleAdDetails);
  };

  const updateSelectedAd = async () => {
    console.log("🚀 ~ updateSelectedAd ~ optimizationId:", optimizationId);
    const response = await axios.put(`/update-selected-ad/${optimizationId}`, {
      selected_ad: optimizedAds[selectedAdIndex],
    });
    console.log("🚀 ~ updateSelectedAd ~ response:", response);
  };

  const handleSelectAd = async (index) => {
    console.log("🚀 ~ handleSelectAd ~ optimizedAds:", optimizedAds);
    setSelectedAdIndex(index);
    updateSelectedAd();
  };

  const handleRegenerateAds = () => {
    handleOptimizeAd();
  };

  const handleCopyAdToText = (ad) => {
    setAdText(ad);
  };

  return (
    <Box sx={{ p: 4 }}>
      <Typography variant="h4" gutterBottom>
        Optimize Your Ad
      </Typography>
      <Typography variant="body1" color="textSecondary" gutterBottom>
        You can use the sample ad below as a reference to create your optimized
        ad. The AI-powered suggestions will help you improve your ad's
        effectiveness.
      </Typography>

      {loadingSample ? (
        <Skeleton variant="rectangular" width={"100%"} height={11} />
      ) : sampleAd ? (
        <Card
          variant="outlined"
          sx={{ mb: 4, backgroundColor: "#f0f4ff", borderRadius: 2 }}
        >
          <CardContent>
            <Typography variant="h6" gutterBottom>
              Sample Optimized Ad
            </Typography>
            <Typography variant="body1" color="textPrimary" gutterBottom>
              {sampleAd}
            </Typography>
            <Divider sx={{ my: 2 }} />
            <Typography variant="body2" color="textSecondary">
              Details: {sampleAdDetails}
            </Typography>
            <Button
              variant="outlined"
              color="primary"
              onClick={handleUseSampleAd}
              sx={{ mt: 2 }}
            >
              Use Sample Ad
            </Button>
          </CardContent>
        </Card>
      ) : null}

      <Typography variant="h6" gutterBottom>
        Select Input Type
      </Typography>
      <FormControl component="fieldset">
        <RadioGroup
          row
          aria-label="input-type"
          value={inputType}
          onChange={(e) => setInputType(e.target.value)}
        >
          <FormControlLabel
            value="text"
            control={<Radio />}
            label="Text Input"
          />
          <FormControlLabel
            value="image"
            control={<Radio />}
            label="Image Input"
          />
        </RadioGroup>
      </FormControl>

      {inputType === "text" ? (
        <TextField
          label="Ad Text"
          multiline
          rows={4}
          fullWidth
          value={adText}
          onChange={handleTextChange}
          margin="normal"
        />
      ) : (
        <Box
          {...getRootProps()}
          sx={{ border: "1px dashed gray", padding: 2, textAlign: "center" }}
        >
          <input {...getInputProps()} />
          {image ? (
            <img
              src={URL.createObjectURL(image)}
              alt="Preview"
              style={{ maxWidth: "100%", marginBottom: "10px" }}
            />
          ) : (
            <Typography variant="body1">
              Drag & Drop Image Here or Click to Select
            </Typography>
          )}
        </Box>
      )}

      <TextField
        label="Ad Details"
        multiline
        rows={4}
        fullWidth
        value={adDetails}
        onChange={handleAdDetailsChange}
        margin="normal"
      />

      <Button
        variant="contained"
        color="primary"
        disabled={loading || (inputType === "text" && !adText)}
        onClick={handleOptimizeAd}
        sx={{ mt: 2 }}
      >
        {loading ? "Optimizing..." : "Optimize Ad"}
      </Button>

      {error && (
        <Typography color="error" sx={{ mt: 2 }}>
          {error}
        </Typography>
      )}

      {optimizedAds.length > 0 && (
        <Box sx={{ mt: 3 }}>
          <Typography variant="h6">Optimized Ads</Typography>
          <Grid container spacing={2}>
            {optimizedAds.map((ad, index) => (
              <Grid item xs={12} md={6} key={index}>
                <Card
                  variant="outlined"
                  sx={{
                    backgroundColor:
                      selectedAdIndex === index ? "#e0f7fa" : "#fff",
                    borderRadius: 2,
                    cursor: "pointer",
                    boxShadow: selectedAdIndex === index ? 3 : 1,
                  }}
                  onClick={() => handleSelectAd(index)}
                >
                  <CardContent>
                    <Typography variant="body1" gutterBottom>
                      {ad}
                    </Typography>
                    <Button
                      variant="outlined"
                      color="primary"
                      onClick={(e) => {
                        e.stopPropagation();
                        handleCopyAdToText(ad);
                      }}
                      sx={{ mt: 2 }}
                    >
                      Copy to Ad Text
                    </Button>
                  </CardContent>
                </Card>
              </Grid>
            ))}
          </Grid>
          <Button
            variant="contained"
            color="secondary"
            onClick={handleRegenerateAds}
            sx={{ mt: 3 }}
          >
            Regenerate Ads
          </Button>
        </Box>
      )}
      <motion.div whileHover={{ scale: 1.05 }}>
        <Button
          variant="outlined"
          color="secondary"
          onClick={() => navigate("/")}
          sx={{ mt: 2, ml: 2 }}
        >
          Go to Previous Ads
        </Button>
      </motion.div>
    </Box>
  );
};

export default OptimizeAd;
