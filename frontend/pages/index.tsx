import React from "react";
import Head from "next/head";
import HeroCreative from "../components/HeroCreative";
import BentoGridDelphi from "../components/BentoGridDelphi";
import DemoCreative from "../components/DemoCreative";
import FooterCreative from "../components/FooterCreative";

export default function Home() {
  return (
    <>
      <Head>
        <title>Abdullah | The Interface to Your Digital Mind</title>
        <meta
          name="description"
          content="Create your digital twin. Scale your expertise. The world's first extensive digital twin engine."
        />
      </Head>

      <HeroCreative />
      <BentoGridDelphi />
      <DemoCreative />
      <FooterCreative />
    </>
  );
}