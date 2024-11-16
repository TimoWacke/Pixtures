<template>
  <div><router-view /></div>
</template>

<script>
export default {
  store: {},
  mounted() {
    document.addEventListener("keyup", function (event) {
      // Number 13 is the "Enter" key on the keyboard
      if (event.keyCode === 13 && !event.shiftKey) {
        // Trigger the button element with a click
        document.getElementById("send").click();
      }
    });
    window.SnipcartSettings = {
      publicApiKey:
        "ODZiOGIwOTMtOTVkOS00OGJjLTliMDUtMjE2MzAwYTJiZDRjNjM4MDI4MzUzMjI4OTQyMjA0",
      loadStrategy: "on-user-interaction",
    };

    (() => {
      var c;
      (c = window.SnipcartSettings).version != null || (c.version = "3.0");
      var s;
      (s = window.SnipcartSettings).timeoutDuration != null ||
        (s.timeoutDuration = 2750);
      var l;
      (l = window.SnipcartSettings).domain != null ||
        (l.domain = "cdn.snipcart.com");
      var w;
      (w = window.SnipcartSettings).protocol != null || (w.protocol = "https");
      var f =
          window.SnipcartSettings.version.includes("v3.0.0-ci") ||
          (window.SnipcartSettings.version != "3.0" &&
            window.SnipcartSettings.version.localeCompare("3.4.0", void 0, {
              numeric: !0,
              sensitivity: "base",
            }) === -1),
        m = ["focus", "mouseover", "touchmove", "scroll", "keydown"];
      window.LoadSnipcart = o;
      document.readyState === "loading"
        ? document.addEventListener("DOMContentLoaded", r)
        : r();
      function r() {
        window.SnipcartSettings.loadStrategy
          ? window.SnipcartSettings.loadStrategy === "on-user-interaction" &&
            (m.forEach((t) => document.addEventListener(t, o)),
            setTimeout(o, window.SnipcartSettings.timeoutDuration))
          : o();
      }
      var a = !1;
      function o() {
        if (a) return;
        a = !0;
        let t = document.getElementsByTagName("head")[0],
          e = document.querySelector("#snipcart"),
          i = document.querySelector(
            `src[src^="${window.SnipcartSettings.protocol}://${window.SnipcartSettings.domain}"][src$="snipcart.js"]`
          ),
          n = document.querySelector(
            `link[href^="${window.SnipcartSettings.protocol}://${window.SnipcartSettings.domain}"][href$="snipcart.css"]`
          );
        e ||
          ((e = document.createElement("div")),
          (e.id = "snipcart"),
          e.setAttribute("hidden", "true"),
          document.body.appendChild(e)),
          v(e),
          i ||
            ((i = document.createElement("script")),
            (i.src = `${window.SnipcartSettings.protocol}://${window.SnipcartSettings.domain}/themes/v${window.SnipcartSettings.version}/default/snipcart.js`),
            (i.async = !0),
            t.appendChild(i)),
          n ||
            ((n = document.createElement("link")),
            (n.rel = "stylesheet"),
            (n.type = "text/css"),
            (n.href = `${window.SnipcartSettings.protocol}://${window.SnipcartSettings.domain}/themes/v${window.SnipcartSettings.version}/default/snipcart.css`),
            t.prepend(n)),
          m.forEach((g) => document.removeEventListener(g, o));
      }
      function v(t) {
        !f ||
          ((t.dataset.apiKey = window.SnipcartSettings.publicApiKey),
          window.SnipcartSettings.addProductBehavior &&
            (t.dataset.configAddProductBehavior =
              window.SnipcartSettings.addProductBehavior),
          window.SnipcartSettings.modalStyle &&
            (t.dataset.configModalStyle = window.SnipcartSettings.modalStyle),
          window.SnipcartSettings.currency &&
            (t.dataset.currency = window.SnipcartSettings.currency),
          window.SnipcartSettings.templatesUrl &&
            (t.dataset.templatesUrl = window.SnipcartSettings.templatesUrl));
      }

      console.log("snipcart install script");
    })();
    document.addEventListener("snipcart.ready", () => {
      console.log("snipcart is ready");
    });
  },
  methods: {
    formatDate(date, format) {
      var dat = new Date(date);
      if (format) {
        format = format.replace("YYYY", dat.getFullYear());
        format = format.replace("YY", dat.getYear());
        format = format.replace(
          "MM",
          (dat.getMonth() + 1 < 10 ? "0" : "") + (dat.getMonth() + 1)
        );
        format = format.replace("M", dat.getMonth() + 1);
        format = format.replace(
          "DD",
          (dat.getDate() < 10 ? "0" : "") + dat.getDate()
        );
        format = format.replace("D", dat.getDate());
        return format;
      }
      const months = [
        "January",
        "February",
        "March",
        "April",
        "May",
        "June",
        "July",
        "August",
        "September",
        "October",
        "November",
        "December",
      ];
      const day = dat.getDate();
      var sib = "th";
      if (day < 4) {
        sib = "rd";
        if (day < 3) sib = "nd";
        if (day == 1) sib = "st";
      }
      return day + sib + " " + months[dat.getMonth()] + " " + dat.getFullYear();
    },
  },
};
</script>



<style lang="scss">
@import url("https://fonts.googleapis.com/css2?family=Nunito&family=Roboto");

$primary: #0f476f;
$secondary: #ff049b;

.sign-page {
  margin: 0;
  height: 80vh;
  display: flex;
  align-items: center;
}

#content,
#iframe,
.sign-page {
  font-family: "Nunito", "Roboto";
  color: $primary;
}

.none {
  display: none !important;
}

.pointer {
  cursor: pointer;
}

#content.site {
  max-width: calc(100% - 120px);
  display: flex;
  justify-content: center;
  padding: 100px 60px 50px 60px;
  margin: 0;
  .wrap {
    min-width: min-content;
  }
}

#content {
  margin: 120px 60px 120px 0;
  @media only screen and (min-width: 1700px) {
    padding-right: 50px;
  }
  padding-right: calc(5vw - 100px);
  display: flex;
  flex-direction: column;
  justify-content: center;

  .wrap {
    display: flex;
    flex-wrap: wrap;
    .project {
      margin-right: 50px;
      min-width: 25vw;
      margin-bottom: auto;
    }
  }
}

h1,
h3 {
  margin: 0px 0 15px;
}

.tight:is(h1, h2, h3) {
  margin: 5px 0;
}

.headers {
  h1,
  h2,
  h3,
  h4 {
    margin-top: 10px;
    margin-bottom: 10px;
    border-radius: 5px;
  }
  h2 {
    padding: 5px 30px 5px 15px;
    color: #fff;
    font-size: 16px;
    background: $secondary;
    @media only screen and (min-width: 800px) {
      background: linear-gradient(120deg, #f0b0 15%, $secondary 20%);
      margin-left: calc(-3vw - 100px);
      padding-left: calc(3vw + 100px);
    }
  }
  h1 {
    @media only screen and (max-width: 800px) {
      font-size: 24px;
    }
  }
  margin-bottom: 50px;
}

.bborder {
  border: 1px solid #000;
  border-radius: 3px;
  background: transparent;
  outline: none;
  padding: 4px;
}

p,
a {
  font-family: "Nunito", "Roboto";
  margin: 0;
  color: $primary;

  @media only screen and (max-height: 800px) {
    &.mobile-white {
      color: #fff;
    }
  }
}

#error {
  color: $secondary;
}
.hidden {
  opacity: 0;
  height: 0;
}

hr.hidden {
  width: 6px;
}

.card {
  padding: 15px;
  margin: 15px auto;
  display: flex;
  width: calc(100% - 30px);
  flex-direction: column;
  justify-content: center;
  background: $primary;
  border-radius: 4px;
  color: #fff;

  input {
    width: calc(100% - 20px);
  }

  div {
    align-self: flex-start;
    text-align: left;
    p,
    a,
    button {
      margin: 5px 0;
      font-size: 16px;
    }
    &.small {
      margin: 5px 12px 10px;
      p,
      a {
        font-size: 12px;
      }
      #error {
        margin-bottom: 5px;
      }
    }
  }

  h2 {
    font-size: 20px;
    align-self: flex-start;
    margin: 8px 0 16px;
  }

  p,
  a {
    color: #fff;
  }

  button {
    background: $secondary;
    color: #fff;
    width: 36%;

    @media only screen and (max-width: 900px) {
      width: 50%;
    }
    @media only screen and (max-width: 600px) {
      width: 100%;
    }
    min-width: 100px;
    &.right {
      margin-top: calc(10px - 1.5vw);
    }
  }
}

.column,
form {
  display: flex;
  flex-direction: column;
}

.right {
  margin-left: auto;
}

.hori {
  display: flex;
  flex-direction: row;
  padding: 0;
  &.zontal {
    align-items: center;
    input,
    select {
      width: 100%;
    }
  }
  &.spce {
    width: 100%;
    justify-content: space-between;
  }

  &.even {
    width: 100%;
    justify-content: space-evenly;
  }

  &.mobile-cmpr {
    @media only screen and (max-width: 900px) {
      flex-direction: column;

      hr,
      p {
        display: none;
      }
    }
  }
  &.d {
    @media only screen and (max-width: 900px) {
      flex-direction: column;
    }
  }
}

.shadow {
  box-shadow: 0px 0px 4px 0px #ddd;
  border-radius: 8px;
  padding: 0 15px;
}

.container {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  width: 61%;

  &.wide {
    width: 90%;
    max-width: 1760px;
  }

  margin: auto;

  @media only screen and (max-width: 800px) {
    width: calc(80% + 30px);
  }

  h1 {
    color: $primary;
  }
  &.tight {
    @media only screen and (min-width: 1200px) {
      width: 50%;
    }

    @media only screen and (min-width: 1650px) {
      width: 40%;
    }
  }
}

div:empty {
  display: none;
}

label {
  margin-top: 10px;
  font-weight: 600;
}
input,
button,
select {
  margin: 5px 0px;
  border: none;
  outline: none;
  &:not([type="color"]) {
    padding: 5px 10px;
  }
  border-radius: 3px;
  white-space: nowrap;
  &:disabled {
    opacity: 0.69;
    cursor: default;
  }
}

button {
  color: #fff;
  cursor: pointer;
  font-weight: bold;
  padding: 5px 10px;
  background-color: $primary;
  &.invert {
    border: 2px solid;
    background-color: #fff;
    color: $primary;
  }
}

.gradient {
  background: linear-gradient(
    20deg,
    rgba(8, 36, 56, 1) 0%,
    rgba(15, 71, 111, 1) 100%
  );
  a,
  * {
    color: #fff;
  }
}

body {
  margin: 0;
}

hr {
  width: 2px;
  height: 64px;
  background: #fff;
  outline: none;
  border: none;
  margin: 0 5px;
}

#frame {
  position: absolute;
  display: flex;
  align-items: flex-end;
  justify-content: center;
  top: 0;
  padding: 0;
  margin: 0;
  height: 100vh;
  width: 100vw;
  overflow: hidden;
  z-index: -1;

  #footer-img {
    width: 100%;
    min-width: 1200px;
    margin-bottom: -15vw;
  }
}

select:not([type="color"]) {
  padding: 4px 8px;
}

#vlogo {
  @media only screen and (min-width: 1700px) {
    position: absolute;
    top: 45px;
    right: 300px;
    width: 210px !important;
  }

  @media only screen and (min-width: 900px) {
    width: calc(150px + 10vw);
    margin: auto calc(-75px - 5vw) calc(5vw - 75px) auto;
  }
  @media only screen and (max-width: 900px) {
    margin: 0 0 0 auto;
  }
}

.content-icon {
  margin-top: 30px;
  height: 30px;
}

.file {
  label {
    display: none;
  }
  .content-icon {
    margin: auto 0 auto 0;
  }
  margin: 10px auto;
}

.pushdown {
  height: 100%;
  display: flex;
  align-items: flex-end;
  button {
    min-width: 100px;
  }
}

.public-layout {
  margin-top: 20px;
  width: 250px;
  p {
    margin-top: 10px;
  }
}

.node {
  display: flex;
  flex-direction: row;
}

#content #details {
  display: flex;
  flex-direction: row !important;
  justify-content: space-between;
  #details {
    margin: 10px;
    label {
      margin-bottom: 10px;
    }
  }

  .field {
    margin: 0px 10px;
    .text-right {
      text-align: right;
    }
  }
}

#content .home #details {
  display: flex;
  flex-direction: column !important;
  #details {
    margin: 0 !important;
  }
  .box {
    .box {
      flex-direction: row !important;
    }
  }
}

.project {
  width: min-content;
}

#content #details #details {
  display: flex;
  flex-wrap: wrap;
  width: auto;
  .field {
    min-width: max-content;
    p {
      max-width: 200px;
      white-space: wrap;
    }
  }
}

#details .box {
  display: flex;

  margin-left: 10px;

  input {
    border: 1px solid #000;
    border-radius: 2px;
    background: transparent;
  }
  .box {
    justify-content: space-between;
    flex-direction: row;
    .field {
      padding-left: 10px;
      p {
        min-width: 100px;
        max-width: 150px;
      }
    }
  }
  .field {
    display: flex;
    flex-direction: column;
  }

  textarea {
    min-height: 50px;
    max-height: calc(15vh + 50px);
    min-width: calc(25vw - 10px);
    max-width: calc(25vw - 10px);
    padding: 5px;
  }

  .draft button {
    margin-bottom: 30px;
    display: flex;
  }
}

@media only screen and (max-width: 800px) {
  .hori.highlvl {
    flex-direction: column;
  }
  #menubtn {
    right: 10px !important;
    position: absolute !important;
    margin: 0;
    padding: 0;
  }

  #content.site {
    max-width: calc(100vw - 30px);
    padding: 100px 15px 50px 15px;
    .wrap {
      flex-direction: column;
      width: 100%;
    }
    .project {
      width: calc(100vw - 30px - 30px);
      overflow: hidden;
      padding: 5px 15px 10px;
      margin: 20px 0;

      h2,
      h3,
      h4 {
        font-size: 14px;
        a {
          font-size: 14px;
        }
        margin: 10px 0 5px;
      }
      font-size: 8px;
      p,
      a,
      label,
      input,
      button,
      select,
      textarea {
        font-size: 10px;
      }
      hr {
        height: 16px;
      }
      .mobile-compr {
        flex-wrap: wrap;
      }
      margin-bottom: 0;
      .dragdrop,
      textarea {
        max-width: calc(100% - 22px) !important;
        min-width: calc(100% - 22px) !important;

        padding: 5px 10px;
      }
      .node:not(.file) {
        margin-left: 0;
        margin-right: 0;

        #details {
          flex-direction: column !important;
          margin-left: 0 !important;
          margin-right: 0 !important;
          div {
            margin-left: 0;
            margin-right: 0;
            div {
              margin-left: 0;
              margin-right: 0;
            }
          }
        }
      }
      .content-icon img {
        width: 20px !important;
        height: 20px !important;
        margin: 5px 10px 0 0;
      }
      button {
        min-width: 66px;
      }
    }
  }
}

#snipcart {
  /* ----------------- 
        Colors
    ----------------- */
  --primary: #0f476f;
  --primaryHover: #18547f;
  --color-default: var(--primary);
  --color-alt: hsl(0, 0%, 50%);
  --color-icon: var(--primary);
  --color-success: hsl(144, 50%, 55%);
  --color-error: hsl(6, 55%, 60%);

  --color-link: var(--primary);
  --color-link-hover: hsl(220, 70%, 65%);
  --color-link-active: var(--color-link);
  --color-link-focus: var(--color-link);

  --color-input: var(--color-default);
  --color-input-hover: var(--color-input);
  --color-input-focus: var(--color-input);
  --color-input-checked: var(--color-input);
  --color-input-disabled: var(--color-alt);
  --color-input-error: var(--color-error);
  --color-inputLabel: var(--color-default);
  --color-inputLabel-hover: var(--color-inputLabel);
  --color-inputLabel-focus: var(--color-inputLabel);
  --color-inputIcon: var(--color-alt);
  --color-inputIcon-hover: var(--color-default);
  --color-inputIcon-focus: var(--color-inputIcon);
  --color-inputIcon-checked: var(--color-default);
  --color-inputIcon-error: var(--color-error);
  --color-inputPlaceholder: var(--color-alt);

  --color-buttonPrimary: #fff;
  --color-buttonPrimary-hover: hsl(0, 0%, 100%);
  --color-buttonPrimary-active: var(--color-buttonPrimary);
  --color-buttonPrimary-focus: var(--color-buttonPrimary);
  --color-buttonPrimary-disabled: var(--color-alt);
  --color-buttonPrimary-success: var(--color-buttonPrimary);
  --color-buttonPrimary-error: var(--color-buttonPrimary);

  --color-buttonSecondary: var(--color-icon);
  --color-buttonSecondary-hover: var(--primaryHover);
  --color-buttonSecondary-active: var(--color-buttonSecondary);
  --color-buttonSecondary-focus: var(--color-buttonSecondary);
  --color-buttonSecondary-disabled: hsl(210, 10%, 25%);
  --color-buttonSecondary-success: var(--color-success);
  --color-buttonSecondary-error: var(--color-error);

  --color-buttonDanger: var(--color-error);
  --color-buttonDanger-hover: hsl(6, 55%, 70%);
  --color-buttonDanger-active: var(--color-buttonDanger);
  --color-buttonDanger-focus: var(--color-buttonDanger);
  --color-buttonDanger-disabled: hsl(210, 10%, 25%);
  --color-buttonDanger-success: var(--color-default);
  --color-buttonDanger-error: var(--color-default);

  --color-badge: var(--color-link);
  --color-badge-active: var(--color-link);
  --color-badge-disabled: var(--color-alt);

  /* ----------------- 
        Border colors
    ----------------- */
  --borderColor-default: hsla(0, 0%, 100%, 10%);
  --borderColor-error: hsl(6, 55%, 30%);

  --borderColor-link: currentColor;
  --borderColor-link-hover: currentColor;
  --borderColor-link-active: currentColor;
  --borderColor-link-focus: currentColor;

  --borderColor-input: hsla(0, 0%, 100%, 10%);
  --borderColor-input-hover: var(--primaryHover);
  --borderColor-input-focus: var(--borderColor-input-hover);
  --borderColor-input-checked: var(--borderColor-input-hover);
  --borderColor-input-disabled: hsl(210, 10%, 20%);
  --borderColor-input-error: var(--borderColor-error);

  --borderColor-buttonPrimary: transparent;
  --borderColor-buttonPrimary-hover: transparent;
  --borderColor-buttonPrimary-focus: transparent;
  --borderColor-buttonPrimary-disabled: transparent;
  --borderColor-buttonPrimary-success: transparent;
  --borderColor-buttonPrimary-error: transparent;

  --borderColor-buttonSecondary: transparent;
  --borderColor-buttonSecondary-hover: transparent;
  --borderColor-buttonSecondary-focus: transparent;
  --borderColor-buttonSecondary-disabled: transparent;
  --borderColor-buttonSecondary-success: transparent;
  --borderColor-buttonSecondary-error: transparent;

  --borderColor-badge: transparent;
  --borderColor-badge-active: transparent;
  --borderColor-badge-disabled: transparent;

  /* ----------------- 
        Background colors
    ----------------- */

  --bgColor-link: none;
  --bgColor-link-hover: none;
  --bgColor-link-active: none;
  --bgColor-link-focus: hsl(210, 55%, 10%);

  --bgColor-input-hover: var(--bgColor-input);
  --bgColor-input-focus: var(--bgColor-input);
  --bgColor-input-checked: var(--borderColor-input-hover);
  --bgColor-input-disabled: hsl(210, 10%, 14%);
  --bgColor-input-error: var(--bgColor-input);
  --bgColor-input-autofill: hsl(210, 60%, 15%);

  --bgColor-buttonPrimary: var(--primary);
  --bgColor-buttonPrimary-hover: var(--primaryHover);
  --bgColor-buttonPrimary-active: var(--bgColor-buttonPrimary);
  --bgColor-buttonPrimary-focus: var(--bgColor-buttonPrimary);
  --bgColor-buttonPrimary-disabled: hsl(210, 10%, 25%);
  --bgColor-buttonPrimary-success: hsl(144, 66%, 30%);
  --bgColor-buttonPrimary-error: hsl(6, 60%, 35%);

  --bgColor-buttonSecondary: var(--bgColor-info);
  --bgColor-buttonSecondary-hover: hsl(210, 60%, 18%);
  --bgColor-buttonSecondary-active: var(--bgColor-buttonSecondary);
  --bgColor-buttonSecondary-focus: var(--bgColor-buttonSecondary);
  --bgColor-buttonSecondary-disabled: hsl(210, 10%, 9%);
  --bgColor-buttonSecondary-success: var(--bgColor-success);
  --bgColor-buttonSecondary-error: var(--bgColor-error);

  --bgColor-buttonDanger: var(--bgColor-error);
  --bgColor-buttonDanger-hover: hsl(6, 50%, 18%);
  --bgColor-buttonDanger-active: var(--bgColor-buttonDanger);
  --bgColor-buttonDanger-focus: var(--bgColor-buttonDanger);
  --bgColor-buttonDanger-disabled: hsl(210, 10%, 9%);
  --bgColor-buttonDanger-success: hsl(144, 66%, 30%);
  --bgColor-buttonDanger-error: hsl(6, 60%, 35%);

  --bgColor-badge: hsl(210, 55%, 10%);
  --bgColor-badge-active: hsl(210, 60%, 15%);
  --bgColor-badge-disabled: hsl(210, 10%, 11%);

  /* ----------------- 
        Shadows
    ----------------- */

  --shadow-default: 0px 20px 24px -20px hsla(0, 0%, 0%, 0.5);
  --shadow-tooltip: 0px 8px 16px hsla(220, 70%, 22%, 0.5);

  --shadow-link-focus: 0px 6px 4px -3px hsla(200, 90%, 40%, 0.5);

  --shadow-input-hover: none;
  --shadow-input-focus: 0px 5px 10px -3px hsla(200, 90%, 40%, 0.3);
  --shadow-input-checked: none;

  --shadow-buttonPrimary-hover: 0px 10px 4px -8px hsla(0, 0%, 0%, 0.5);
  --shadow-buttonPrimary-active: none;
  --shadow-buttonPrimary-focus: 0px 0px 6px 2px hsl(200, 90%, 40%);

  --shadow-buttonSecondary-hover: 0px 10px 4px -8px hsla(0, 0%, 0%, 0.2);
  --shadow-buttonSecondary-active: none;
  --shadow-buttonSecondary-focus: 0px 0px 6px 2px hsla(200, 90%, 40%, 0.8);

  --shadow-buttonDanger-hover: 0px 10px 4px -8px hsla(0, 0%, 0%, 0.25);
  --shadow-buttonDanger-active: none;
  --shadow-buttonDanger-focus: 0px 0px 6px 2px hsla(6, 55%, 60%);
}
</style>
