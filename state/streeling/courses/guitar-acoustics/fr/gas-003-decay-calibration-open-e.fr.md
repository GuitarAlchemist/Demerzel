---
module_id: gas-003-decay-calibration-open-e
department: guitar-acoustics
course: "Calibrer un test de décroissance du mi à vide pour le moteur de guitare GA"
level: intermediate
alchemical_stage: albedo
prerequisites: [gas-001-open-string-audio-evidence]
estimated_duration: "40 minutes"
produced_by: codex-project-pilot
research_cycle: guitar-acoustics-2026-10-12-003
version: "0.1.0"
---

# Calibrer un test de décroissance du mi à vide pour le moteur de guitare GA

> **Département d'acoustique et de synthèse de guitare** | Intermédiaire | 40 minutes | Traduction IA provisoire ; révision en attente

## Objectifs

Vous distinguerez une *mesure* de décroissance d'un *paramètre* Rust, calculerez l'écart de la paire de mi à vide épinglée, suivrez le coefficient de rétroaction du moteur et définirez une expérience native à un seul paramètre, avec critère de réfutation et garde-fous. [GAS-001](../en/gas-001-open-string-audio-evidence.md) établit la paire enregistrée et synthétisée ; [GAS-002](../en/gas-002-brightness-control-and-evaluation-gate.md) examine une hypothèse de brillance sur un rapport harmonique local. Ici, la question est : **une modification contrôlée de la décroissance GA rapproche-t-elle la baisse de niveau du mi à vide de celle de l'enregistrement, sans dégrader l'attaque, la hauteur ou les autres notes ?** Aucun candidat de décroissance n'a été rendu pour cette leçon.

## 1. Partir de l'enveloppe mesurée, pas du réglage

La [fixture GAS-001](https://github.com/GuitarAlchemist/Demerzel/tree/5c4967454ddc740ed937c87719ca4d71a3522e4b/state/streeling/fixtures/guitar-acoustics/gas-001) épinglée contient deux WAV mono de quatre secondes à 44 100 Hz : un enregistrement acoustique distinct, étiqueté mi2 à vide par son jeu de données, et un rendu **natif** du moteur Rust GA à la révision `dc2e74cbd992a298f67efb928b5b3754615e1924`. Le rendu utilise le profil de guitare 0 par défaut et `engine_note_on(82.4069 Hz, velocity 0.1)`. Ce n'est pas une capture de l'AudioWorklet du navigateur. Le [README de la fixture](https://github.com/GuitarAlchemist/Demerzel/blob/5c4967454ddc740ed937c87719ca4d71a3522e4b/state/streeling/fixtures/guitar-acoustics/gas-001/README.md) donne les empreintes des WAV, les limites de provenance, le crédit de la source et l'attribution CC BY-SA 4.0 de l'enregistrement.

Le [JSON de mesures](https://github.com/GuitarAlchemist/Demerzel/blob/5c4967454ddc740ed937c87719ca4d71a3522e4b/state/streeling/fixtures/guitar-acoustics/gas-001/measurements.json) indique une variation RMS tardive moins précoce de **−3.9 dB** pour l'enregistrement et de **−1.1 dB** pour le rendu. Le [script de mesure](https://github.com/GuitarAlchemist/Demerzel/blob/5c4967454ddc740ed937c87719ca4d71a3522e4b/state/streeling/fixtures/guitar-acoustics/gas-001/measure-pair.py) prend les fenêtres 0.2–0.4 s et 1.0–1.2 s **après la première attaque de chaque fichier**. La première attaque enregistrée arrive vers 1.1 s et une autre vers 2.75 s ; le rendu commence à zéro. Les fenêtres enregistrées correspondent donc environ à **1.3–1.5** et **2.1–2.3 s** dans le fichier, avant la deuxième attaque. Ce ne sont pas des constantes de décroissance du fichier entier.

La baisse sélectionnée du rendu est **moins négative de 2.8 dB** : `−1.1 − (−3.9) = +2.8 dB`. Son erreur absolue par rapport à la variation enregistrée vaut `|−1.1 − (−3.9)| = 2.8 dB`. Ces valeurs sont déjà arrondies au dixième. Les WAV diffèrent par leur niveau initial, leur instrument, leur microphone, leur pièce et leur pincement : comparer les *variations* de niveau dans chaque fichier est plus utile ici que comparer directement les RMS absolus en dBFS. Cet écart n'identifie pourtant ni le paramètre responsable, ni la préférence des auditeurs.

### Exercice 1 — Lire l'écart

Calculez, avec les valeurs sauvegardées, la différence signée rendu moins enregistrement pour la variation tardive moins précoce, puis l'erreur absolue. Une erreur de 2.8 dB signifie-t-elle que le rendu entier est 2.8 dB plus fort ?

> **Réponse :** `−1.1 − (−3.9) = +2.8 dB` ; l'erreur absolue vaut `2.8 dB`. Le niveau du rendu baisse moins entre les deux fenêtres RMS alignées sur l'attaque. Ce n'est ni une comparaison de sonie des fichiers entiers ni une preuve de préférence auditive.

### Exercice 2 — Exclure la deuxième attaque

À quels instants du fichier se situent les deux fenêtres de l'enregistrement si la première attaque est vers 1.1 s ? Pourquoi une fenêtre tardive commençant à 2.8 s ne convient-elle pas à cette première note ?

> **Réponse :** La fenêtre précoce vaut environ `1.1 + [0.2, 0.4] = 1.3–1.5 s` ; la tardive, `1.1 + [1.0, 1.2] = 2.1–2.3 s`. À 2.8 s, elle suivrait l'autre attaque, située vers 2.75 s, et mêlerait un nouvel événement à la décroissance supposée. Le point d'attaque étant approximatif, refaites la mesure avec une petite variation de ce point avant toute affirmation forte.

## 2. Suivre le paramètre Rust et le coefficient effectif

Dans le [moteur Rust GA](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/Rust/guitar-web-wasm-demo/rust-engine/src/lib.rs) épinglé, `Engine::new` commence avec `decay = 0.9968`, puis sélectionne le profil 0 par défaut, qui fixe la **décroissance de base à 0.9978**. La fonction exportée `engine_set_decay` limite la valeur demandée à `[0.95, 0.9999]`. Choisissez le profil **avant** d'appliquer une valeur candidate : un changement de profil ultérieur réécrit la décroissance et d'autres réglages. Le [programme de rendu de la fixture](https://github.com/GuitarAlchemist/Demerzel/blob/5c4967454ddc740ed937c87719ca4d71a3522e4b/state/streeling/fixtures/guitar-acoustics/gas-001/render-ga-e2.py) appelle `engine_init` et `engine_note_on`, mais pas `engine_set_decay` ; il faut donc documenter une extension ou un autre banc d'essai. Aucun rendu candidat n'est rapporté ici.

Les expressions pertinentes dans la boucle de rendu sont :

```text
f_norm = clamp((voice_frequency_hz - 82) / (330 - 82), 0, 1)
voice.sustain = min(0.995 + 0.006 * (1 - f_norm), 0.9998)  # assigned at note excitation
feedback_decay = (base_decay + 0.0025 * (1 - f_norm)) * voice.sustain
```

Pour la fréquence nominale `82.4069 Hz`, `f_norm ≈ 0.00164073`. L'expression non plafonnée de sustain vaut environ `1.00099016` ; `voice.sustain = 0.9998` après plafonnement. Avec `0.9978` en base, le calcul donne `(0.9978 + 0.0025 × (1 − 0.00164073)) × 0.9998 ≈ 1.00009584`. Une valeur de base **proposée** de `0.9976` donne environ **0.99989588**. Les deux valeurs de base sont dans la plage acceptée par le setter.

Ces valeurs sont des **coefficients de rétroaction calculés à partir du code source**, et non des taux de décroissance d'enveloppe mesurés. La boucle mêle aussi des échantillons de ligne à retard, une dispersion passe-tout, un filtre passe-bas à état, la brillance, un bruit d'attaque, des résonateurs et de la réverbération. Un coefficient légèrement supérieur à un dans une expression ne prouve **ni** une sortie instable **ni** un défaut audible. Le réduire ne prédit pas non plus une variation en dB du WAV. Il faut mesurer la sortie selon une méthode fixe.

`attack_decay` régit séparément l'évolution du bruit d'attaque, `reverb_mix` la queue et la brillance le mélange dans la rétroaction. Ne les changez pas en même temps que la décroissance : la cause d'un éventuel effet deviendrait ambiguë. GAS-002 traite déjà de la brillance ; elle reste fixe ici.

### Exercice 3 — Calculer, puis limiter l'inférence

À `82.4069 Hz`, quel plafond de sustain s'applique et quels coefficients effectifs approximatifs obtient-on pour `0.9978` et `0.9976` ? La première valeur, supérieure à un, prouve-t-elle que le WAV GA enregistré devient plus fort au fil du temps ?

> **Réponse :** `f_norm ≈ 0.00164073` ; l'expression non plafonnée dépasse `0.9998`, donc le plafond vaut `0.9998`. Le calcul donne environ `1.00009584` pour `0.9978` et `0.99989588` pour `0.9976`. Non : ce coefficient appartient à un système filtré, à état, résonant et réverbérant. Dans les fenêtres retenues, le WAV sauvegardé affiche au contraire `−1.1 dB` ; le coefficient ne prédit pas seul son enveloppe.

## 3. Déclarer à l'avance une expérience à un seul paramètre

Un essai natif contrôlé compilerait **la même révision Rust épinglée** et initialiserait un moteur neuf pour chaque bras à 44 100 Hz. Gardez le profil 0, la fréquence mi2 `82.4069 Hz`, la vélocité `0.1`, une durée de quatre secondes, le compilateur, l'encodage WAV et tous les autres réglages. Le bras de référence utilise `0.9978`. Dans le bras candidat, appelez `engine_set_decay(0.9976)` **après** l'initialisation et le choix du profil, **avant** `engine_note_on`. Consignez l'ordre des appels et la valeur, les empreintes des deux WAV et le choix du point d'attaque. Le code initialise une graine de bruit fixe ; des moteurs neufs et une compilation identique restent nécessaires pour éviter le report d'état. Le programme actuel n'offre aucune option de décroissance : adaptez-le ou remplacez-le, puis relisez ce code avant toute conclusion empirique. Une comparaison native ne certifie pas l'AudioWorklet du navigateur ; testez-le séparément s'il est destiné à être livré.

Appliquez la même mesure aux deux bras. Un **seuil pédagogique proposé** exige une erreur absolue au moins **1.0 dB inférieure** à l'erreur de référence arrondie de `2.8 dB`, soit `≤ 1.8 dB` autour des `−3.9 dB` enregistrés. Sur les valeurs arrondies, la baisse candidate devrait être entre **−5.7 et −2.1 dB**. Pour décider réellement, utilisez les mesures WAV non arrondies et consignez une tolérance ; ne tranchez pas sur une limite au dixième de dB à partir du JSON arrondi. Ce seuil est un choix pédagogique préalable, **pas** une norme produit GA ni une prédiction de réussite pour `0.9976`.

Ajoutez des garde-fous : ni écrêtage ni quasi-écrêtage (amplitude de crête absolue proposée **inférieure à 0.95**), fondamentale mi2 proche de la référence selon la même recherche de pic sur une seconde, attaque initiale et traces des deuxième et quatrième partiels préservées. Une meilleure RMS globale pourrait masquer un transitoire ou une queue spectrale abîmés. Répétez sur d'autres cordes, notes et vélocités avant de généraliser. Examinez des jugements d'écoute à niveau égalisé et en aveugle : une proximité numérique avec une guitare externe ne démontre pas le réalisme perçu. Si le candidat rate le seuil `≤1.8 dB` ou un garde-fou, rejetez **ce réglage candidat pour ce test** et consignez le résultat mesuré. Cet échec ne prouverait pas qu'aucun changement de décroissance ne peut aider.

### Exercice 4 — Appliquer le seuil proposé

Avec les valeurs de référence arrondies, quelle erreur absolue maximale correspond à une amélioration de 1.0 dB ? Quel intervalle de baisse candidate en résulte autour de `−3.9 dB` ? Un candidat dans cet intervalle mais avec une crête de `0.98` franchirait-il tous les garde-fous ?

> **Réponse :** `2.8 − 1.0 = 1.8 dB` ; `|candidate − (−3.9)| ≤ 1.8` donne `−5.7 ≤ candidate ≤ −2.1 dB`. Une crête de `0.98` échoue au garde-fou proposé `<0.95`, même si la baisse passe. Il s'agit du calcul d'un seuil proposé, pas d'une mesure de candidat.

### Exercice 5 — Formuler une réfutation

Un agent affirme que réduire la valeur de base à `0.9976` améliore l'amortissement mi2 de GA. Quels sont les artefacts contrôlés minimaux et quel résultat réfuterait cette affirmation selon le seuil de la leçon ? Que resterait-il inconnu après un essai réussi sur un seul mi2 ?

> **Réponse :** Conservez la révision et la compilation exactes du moteur, l'ordre des appels de paramètres, les WAV natifs de référence et candidat issus de moteurs neufs et leurs empreintes, ainsi que les mesures alignées sur l'attaque et les contrôles de crête, partiels et attaque. Si l'erreur absolue non arrondie ne diminue pas d'au moins 1.0 dB, ou si un garde-fou échoue, ce candidat rate le seuil. Même en cas de réussite, la sortie navigateur, les autres notes et vélocités, les écarts de prise de son et les préférences des auditeurs resteraient inconnus.

## 4. Séparer amélioration et calibration

L'enregistrement sert de **sonde de calibration**, pas de cible physique exacte pour toutes les guitares. Le jeu de données l'étiquette mi2 à vide, mais sa pièce, son instrument, son microphone et son interprète diffèrent du rendu. Une modification globale de `decay` peut affecter beaucoup de notes ; la formule dépendante de la fréquence rend l'extrapolation depuis mi2 particulièrement fragile. Si le candidat rapproche l'enveloppe de cette référence, dites seulement qu'il rapproche **la variation tardive moins précoce spécifiée** pour ce rendu. Sinon, conservez l'essai raté pour étudier ensuite le bruit d'attaque, la réverbération, la rétroaction selon la fréquence ou la sensibilité aux fenêtres, sans réécrire l'historique.

La [boucle d'itération hors ligne](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/Rust/guitar-web-wasm-demo/full-auto.ps1) de GA et son critique spectral peuvent appuyer des essais répétés, sans donner de verdict automatique d'écoute. Un candidat traité ultérieurement par ComfyUI constituerait un **bras hors ligne distinct**, et non une preuve de succès du setter Rust. Gardez séparés les propositions des agents, rendus, références, empreintes, mesures, révisions et état de publication.

## Sources et limites

- [Provenance GAS-001](https://github.com/GuitarAlchemist/Demerzel/blob/5c4967454ddc740ed937c87719ca4d71a3522e4b/state/streeling/fixtures/guitar-acoustics/gas-001/README.md), [mesures](https://github.com/GuitarAlchemist/Demerzel/blob/5c4967454ddc740ed937c87719ca4d71a3522e4b/state/streeling/fixtures/guitar-acoustics/gas-001/measurements.json), [méthode](https://github.com/GuitarAlchemist/Demerzel/blob/5c4967454ddc740ed937c87719ca4d71a3522e4b/state/streeling/fixtures/guitar-acoustics/gas-001/measure-pair.py) et [rendu natif](https://github.com/GuitarAlchemist/Demerzel/blob/5c4967454ddc740ed937c87719ca4d71a3522e4b/state/streeling/fixtures/guitar-acoustics/gas-001/render-ga-e2.py), tous à la révision Demerzel `5c4967454ddc740ed937c87719ca4d71a3522e4b`.
- [Code source du moteur Rust GA](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/Rust/guitar-web-wasm-demo/rust-engine/src/lib.rs) et [script d'itération hors ligne](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/Rust/guitar-web-wasm-demo/full-auto.ps1), à la révision GA `dc2e74cbd992a298f67efb928b5b3754615e1924`.
- Seule la paire GAS-001 sauvegardée a été mesurée avant cette leçon. Les coefficients et l'intervalle d'acceptation sont calculés. Une vérification indépendante du sujet et de la cohérence des traductions par IA n'a relevé aucun écart exploitable. Le candidat `0.9976`, l'extension du banc natif, la capture navigateur, les contrôles sur plusieurs notes, le panel d'écoute, la revue humaine, le test auprès d'apprenants, la validation linguistique et la publication restent à faire.
