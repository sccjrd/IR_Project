import { Box, Typography, Link, IconButton } from "@mui/material";
import {
  Brightness7 as Brightness7Icon,
  Brightness4 as Brightness4Icon,
} from "@mui/icons-material";

function Header({ setDefinitionOpen, toggleColorMode, mode }) {
  return (
    <Box
      sx={{
        textAlign: "center",
        py: 6,
        position: "relative",
      }}
    >
      <Box
        sx={{
          position: "absolute",
          right: 16,
          top: 16,
        }}
      >
        <IconButton
          onClick={toggleColorMode}
          color="inherit"
          aria-label="toggle dark mode"
        >
          {mode === "dark" ? <Brightness7Icon /> : <Brightness4Icon />}
        </IconButton>
      </Box>

      <Typography
        variant="h3"
        component="h1"
        sx={{
          fontWeight: 600,
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          mb: 1,
          flexWrap: "wrap",
          gap: 1,
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
