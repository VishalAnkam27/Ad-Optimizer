export const fetchCompanies = async () => {
  // Placeholder data for companies
  return [
    { company_id: "UNR123", company_name: "UrbanNest Realty" },
    { company_id: "GAP456", company_name: "Green Acres Properties" },
    // Additional companies
  ];
};

export const fetchProperties = async (companyId) => {
  // Placeholder properties data for given company ID
  return [
    { property_id: "PROP123", property_name: "Property 1" },
    { property_id: "PROP456", property_name: "Property 2" },
  ];
};

export const createProperty = async (companyId, name, details) => {
  // API call to create a new property
  return { success: true };
};

export const fetchPreviousAds = async (companyId, propertyId) => {
  // Placeholder previous ads data
  return [
    { ad_text: "Sample Ad 1", date: "2023-10-10" },
    { ad_text: "Sample Ad 2", date: "2023-11-10" },
  ];
};

export const optimizeAd = async (data) => {
  // Placeholder optimized ads response
  return {
    optimized_ads: ["Optimized Ad 1", "Optimized Ad 2", "Optimized Ad 3"],
  };
};
