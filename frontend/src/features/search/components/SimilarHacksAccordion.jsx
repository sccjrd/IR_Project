import { useState } from "react";
import {
  Accordion,
  AccordionSummary,
  AccordionDetails,
  Typography,
  CircularProgress,
  Stack,
  Link,
  Box,
} from "@mui/material";
import ExpandMoreIcon from "@mui/icons-material/ExpandMore";
import { useSimilar } from "../hooks/useSimilar";

function SimilarHacksAccordion({ hackId }) {
  if (!hackId) return null;

  const [expanded, setExpanded] = useState(false);
  const { similar, loading, error, fetchSimilar } = useSimilar(hackId, {
    limit: 6,
  });

  const handleChange = (_event, isExpanded) => {
    setExpanded(isExpanded);
    if (isExpanded) {
      fetchSimilar();
    }
  };

  const safeSimilar = Array.isArray(similar) ? similar : [];
  const count = safeSimilar.length;

  return (
    <Accordion
      expanded={expanded}
      onChange={handleChange}
      sx={{ mt: 1.5, boxShadow: "none" }}
    >
      <AccordionSummary expandIcon={<ExpandMoreIcon />}>
        <Typography variant="body2" sx={{ fontWeight: 500 }}>
          Similar hacks
        </Typography>
      </AccordionSummary>
      <AccordionDetails>
        {loading && (
          <Box sx={{ display: "flex", alignItems: "center", gap: 1, mb: 0.5 }}>
            <CircularProgress size={18} />
            <Typography variant="caption">Loading similar hacks…</Typography>
          </Box>
        )}

        {error && (
          <Typography variant="caption" color="error">
            {error}
          </Typography>
        )}

        {!loading && !error && count === 0 && (
          <Typography variant="caption" color="text.secondary">
            No similar hacks found.
          </Typography>
        )}

        {!loading && !error && count > 0 && (
          <Stack spacing={0.5}>
            {safeSimilar.map((hack) => (
              <Typography
                key={hack.id || hack.url}
                variant="body2"
                sx={{
                  fontSize: 13,
                  overflow: "hidden",
                  textOverflow: "ellipsis",
                  whiteSpace: "nowrap",
                }}
              >
                <Link
                  href={hack.url}
                  target="_blank"
                  rel="noopener noreferrer"
                  underline="hover"
                >
                  {hack.title || hack.url}
                </Link>
              </Typography>
            ))}
          </Stack>
        )}
      </AccordionDetails>
    </Accordion>
  );
}

export default SimilarHacksAccordion;
