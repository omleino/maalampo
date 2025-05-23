import streamlit as st
import matplotlib.pyplot as plt

def laske_kustannukset(investointi, omaisuuden_myynti, korko, sahkon_hinta, sahkon_kulutus_kwh, laina_aika):
    lainan_maara = investointi - omaisuuden_myynti
    lyhennys = lainan_maara / laina_aika
    jaljella_oleva_laina = lainan_maara

    kustannukset = []
    for _ in range(laina_aika):
        korko_vuodelta = jaljella_oleva_laina * (korko / 100)
        sahkolasku = sahkon_hinta * sahkon_kulutus_kwh
        kokonais = lyhennys + korko_vuodelta + sahkolasku
        kustannukset.append(kokonais)
        jaljella_oleva_laina -= lyhennys
    return kustannukset

def main():
    st.title("Maalämpö vs Kaukolämpö -vertailulaskuri")

    with st.sidebar:
        st.header("Syötteet")
        investointi = st.number_input("Investoinnin suuruus (€)", value=650000.0)
        omaisuuden_myynti = st.number_input("Omaisuuden myyntitulo (€)", value=100000.0)
        korko = st.number_input("Lainan korko (%)", value=3.0)
        sahkon_hinta = st.number_input("Sähkön hinta (€/kWh)", value=0.12)
        sahkon_kulutus = st.number_input("Maalämmön sähkönkulutus (kWh/v)", value=180000.0)
        kaukolampo_kustannus = st.number_input("Kaukolämmön vuosikustannus (€)", value=85000.0)
        laina_aika = st.slider("Laina-aika (vuotta)", 5, 40, value=20)
        maksavat_neliot = st.number_input("Maksavat neliöt (m²)", value=1000.0)

    vuodet = list(range(1, laina_aika + 1))
    kaukolampo = [kaukolampo_kustannus] * laina_aika
    maalampo_ilman = laske_kustannukset(investointi, 0, korko, sahkon_hinta, sahkon_kulutus, laina_aika)
    maalampo_myynnilla = laske_kustannukset(investointi, omaisuuden_myynti, korko, sahkon_hinta, sahkon_kulutus, laina_aika)

    # Ensimmäisen vuoden vastike- ja kuukausierä
    lainan_maara = investointi - omaisuuden_myynti
    lyhennys = lainan_maara / laina_aika
    korko_vuosi = lainan_maara * (korko / 100)
    sahko_vuosi = sahkon_hinta * sahkon_kulutus

    lyh_m2 = lyhennys / maksavat_neliot
    korko_m2 = korko_vuosi / maksavat_neliot
    sahko_m2 = sahko_vuosi / maksavat_neliot
    yhteensa_vuosi = lyh_m2 + korko_m2 + sahko_m2
    yhteensa_kk = yhteensa_vuosi / 12

    kaukolampo_m2 = kaukolampo_kustannus / maksavat_neliot
    kaukolampo_kk = kaukolampo_m2 / 12

    st.subheader("Ensimmäisen vuoden vastikelaskelma")
    st.markdown(f"**Lyhennys:** {lyh_m2:.2f} €/m²/v")
    st.markdown(f"**Korko:** {korko_m2:.2f} €/m²/v")
    st.markdown(f"**Sähkö:** {sahko_m2:.2f} €/m²/v")
    st.markdown(f"**Yhteensä:** {yhteensa_vuosi:.2f} €/m²/v eli {yhteensa_kk:.2f} €/m²/kk")

    st.markdown("---")
    st.markdown(f"**Kaukolämpövastike:** {kaukolampo_m2:.2f} €/m²/v eli {kaukolampo_kk:.2f} €/m²/kk")
    st.markdown(f"**Erotus:** {kaukolampo_m2 - yhteensa_vuosi:.2f} €/m²/v")

    # Kaavio
    fig, ax = plt.subplots()
    ax.plot(vuodet, kaukolampo, label="Kaukolämpö", linestyle="--")
    ax.plot(vuodet, maalampo_ilman, label="Maalämpö (ilman omaisuuden myyntiä)")
    ax.plot(vuodet, maalampo_myynnilla, label="Maalämpö (myynnillä)")
    ax.set_title("Vuosikustannukset vertailussa")
    ax.set_xlabel("Vuosi")
    ax.set_ylabel("Kustannus (€)")
    ax.grid(True)
    ax.legend()
    st.pyplot(fig)

if __name__ == "__main__":
    main()
