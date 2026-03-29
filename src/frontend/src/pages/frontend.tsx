import Link from "next/link";
import { useTranslation } from "react-i18next";
import { ProConnectButton } from "@gouvfr-lasuite/ui-kit";
import { login } from "@/features/auth";
import { AppLayout } from "@/features/layouts/components/main/layout";
import { LeftPanel } from "@/features/layouts/components/main/left-panel";
import { LanguagePicker } from "@/features/layouts/components/main/language-picker";
import { SKIP_LINK_TARGET_ID } from "@/features/ui/components/skip-link";
import { useTheme } from "@/features/providers/theme";

export default function FrontendPage() {
  const { t } = useTranslation();
  const { theme, variant } = useTheme();

  return (
    <AppLayout
      hideLeftPanelOnDesktop
      leftPanelContent={<LeftPanel />}
      rightHeaderContent={<LanguagePicker />}
      icon={<img src={`/images/${theme}/app-logo-${variant}.svg`} alt="logo" height={40} />}
    >
      <main id={SKIP_LINK_TARGET_ID} className="app__frontend">
        <section className="app__frontend__hero">
          <span className="app__frontend__badge">{t("Frontend")}</span>
          <h1>{t("A modern frontend for your messaging workspace")}</h1>
          <p>
            {t(
              "Manage conversations, keep your team aligned and collaborate quickly from a clean interface.",
            )}
          </p>
          <div className="app__frontend__actions">
            <ProConnectButton onClick={login} />
            <Link className="app__frontend__link" href="/">
              {t("Back to home")}
            </Link>
          </div>
        </section>

        <section className="app__frontend__grid" aria-label={t("Frontend highlights")}>
          <article>
            <h2>{t("Fast")}</h2>
            <p>{t("Built with Next.js for quick navigation and a responsive experience.")}</p>
          </article>
          <article>
            <h2>{t("Accessible")}</h2>
            <p>{t("Designed with keyboard navigation and clear hierarchy in mind.")}</p>
          </article>
          <article>
            <h2>{t("Ready for scale")}</h2>
            <p>{t("A structured layout to support inbox, domain and administration workflows.")}</p>
          </article>
        </section>
      </main>
    </AppLayout>
  );
}
