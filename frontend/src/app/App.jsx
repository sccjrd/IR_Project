import SearchPage from "../features/search/components/SearchPage.jsx";
import { Header, Footer } from "../shared/components";
import { useState } from "react";

function App({ toggleColorMode, mode }) {
  const [definitionOpen, setDefinitionOpen] = useState(false);

  return (
    <div style={{ flex: 1, display: "flex", flexDirection: "column" }}>
      <div style={{ flex: 1 }}>
        <Header setDefinitionOpen={setDefinitionOpen} />
        <SearchPage
          setDefinitionOpen={setDefinitionOpen}
          definitionOpen={definitionOpen}
        />
      </div>
      <Footer toggleColorMode={toggleColorMode} mode={mode} />
    </div>
  );
}

export default App;
