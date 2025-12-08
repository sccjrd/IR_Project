import { Box, Typography, Link } from "@mui/material";

function Header({ setDefinitionOpen }) {
  return (
    <Box sx={{ textAlign: "center", mb: 4, py: 6 }}>
      <Typography
        variant="h3"
        component="h1"
        sx={{
          fontWeight: 600,
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          mb: 1,
        }}
      >
        <Box
          component="img"
          src="/ikea-logo.jpg"
          alt="IKEA"
          sx={{ height: "1.5em", verticalAlign: "middle", mr: 1 }}
        />
        Hacks Search
      </Typography>
      <Typography variant="subtitle1" color="text.secondary">
        Search across{" "}
        <Link
          variant="subtitle1"
          onClick={() => setDefinitionOpen(true)}
          sx={{
            cursor: "pointer",
            textDecoration: "underline",
            textDecorationStyle: "dotted",
            textUnderlineOffset: 2,
            "&:hover": {
              textDecorationStyle: "solid",
            },
          }}
        >
          IKEA hacks
        </Link>{" "}
        from multiple websites and{" "}
        <Link
          target="_blank"
          rel="noopener noreferrer"
          href="https://www.reddit.com/r/ikeahacks/"
        >
          r/ikeahacks
        </Link>
      </Typography>
    </Box>
  );
}

export default Header;
