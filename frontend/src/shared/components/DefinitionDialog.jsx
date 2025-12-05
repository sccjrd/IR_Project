import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Button,
  Typography,
  Box,
  IconButton,
} from "@mui/material";
import OpenInNewIcon from "@mui/icons-material/OpenInNew";
import useMediaQuery from "@mui/material/useMediaQuery";
import { useTheme } from "@mui/material/styles";

function DefinitionDialog({ open, onClose }) {
  const theme = useTheme();
  const fullScreen = useMediaQuery(theme.breakpoints.down("md"));

  return (
    <Dialog
      open={open}
      onClose={onClose}
      fullScreen={fullScreen}
      PaperProps={{
        sx: {
          borderRadius: 2,
        },
      }}
    >
      <DialogTitle id="responsive-dialog-title">
        <Typography variant="h5" component="div" sx={{ fontWeight: 600 }}>
          What is an IKEA hack?
        </Typography>
        <IconButton
          aria-label="open source"
          component="a"
          href="https://www.obi.ch/it/magazine/abitare/design-degli-interni/upcycling-per-mobili/hack-ikea"
          target="_blank"
          rel="noopener noreferrer"
          sx={{
            position: "absolute",
            right: 8,
            top: 8,
            color: (theme) => theme.palette.grey[500],
          }}
        >
          <OpenInNewIcon />
        </IconButton>
      </DialogTitle>

      <DialogContent dividers>
        <Box sx={{ py: 1 }}>
          <Typography variant="body1" paragraph>
            There are many ways to make creative furniture on your own. For
            example, there are so-called hacks that allow you to customize your
            IKEA furniture. The term "hack," used to describe technical talent,
            actually comes from the IT sector, but it refers to small changes
            with a big impact on interior design when applied to furniture from
            the Swedish furniture chain.
          </Typography>

          <Typography variant="body1" paragraph>
            With a few simple steps and the right materials, you can recreate,
            renovate, and embellish both old and new IKEA furniture according to
            your wishes, for example, to create more space or seating.
          </Typography>

          <Typography variant="body1" paragraph>
            This brings multifunctional furniture and attractive objects to life
            that match your interior design style. Modern country style and
            shabby chic furniture are particularly popular. Discover original
            ideas and transform your IKEA furniture into truly unique pieces.
          </Typography>
        </Box>
      </DialogContent>

      <DialogActions sx={{ px: 3, py: 2 }}>
        <Button onClick={onClose} variant="contained" color="primary">
          Got it
        </Button>
      </DialogActions>
    </Dialog>
  );
}

export default DefinitionDialog;
