---
module_id: aud-001-eq-compression-order
department: audio-engineering
course: "Fondamentaux de la compression — ratio, seuil, attaque, relâchement"
level: intermediate
prerequisites: []
estimated_duration: "35 minutes"
produced_by: seldon-research-cycle
research_cycle: audio-engineering-2026-03-23-001
version: "1.0.0"
---

# EQ et compression : pourquoi l'ordre de la chaîne de signal compte

> **Département d'ingénierie audio** | Niveau : Intermédiaire | Durée : 35 minutes

## Objectifs
- Comprendre les différences techniques entre les chaînes Comp→EQ et EQ→Comp
- Identifier quand chaque ordre produit de meilleurs résultats sur les voix
- Appliquer la technique du sandwich EQ→Comp→EQ pour un contrôle maximal
- Reconnaître les artefacts de compression dépendants de la fréquence et savoir les prévenir

---

## 1. La question fondamentale

L'ordre entre compression et égalisation a-t-il de l'importance ? **Oui** — de façon mesurable. L'ordre modifie la manière dont le compresseur réagit au contenu fréquentiel, ce qui affecte le naturel de la dynamique et la clarté du timbre.

La raison est simple : un compresseur réagit au *niveau*. Si certaines fréquences sont plus fortes (par exemple l'effet de proximité qui amplifie les 100-200 Hz, ou la sibilance qui culmine entre 4 et 10 kHz), le compresseur réagit à *ces fréquences*, et non à la performance vocale dans son ensemble.

---

## 2. Compression avant EQ (Comp→EQ)

```
Voix → [Compresseur] → [EQ] → Bus de mixage
```

**Ce qui se passe :**
- Le compresseur reçoit le signal brut — y compris les fréquences problématiques
- Si la sibilance est forte (pics entre 4-10 kHz), elle peut déclencher la compression sur ces transitoires
- Le compresseur « pompe » sur les fréquences problématiques au lieu de contrôler la dynamique globale
- L'EQ en aval façonne le signal déjà compressé

**Quand l'utiliser :**
- Quand la voix est bien enregistrée avec peu de problèmes fréquentiels
- Quand on veut que le compresseur réagisse au signal naturel complet
- Quand on utilise une compression douce (ratio 2:1, attaque lente) pour la « cohésion »

**Risque :** Pompage dépendant de la fréquence. Le compresseur ne sait pas que vous ne voulez pas qu'il réagisse à la bosse de proximité à 200 Hz — il ne voit que le niveau.

---

## 3. EQ avant compression (EQ→Comp)

```
Voix → [EQ] → [Compresseur] → Bus de mixage
```

**Ce qui se passe :**
- L'EQ corrective supprime d'abord les problèmes : coupe la proximité à 200 Hz, atténue la sibilance à 6 kHz
- Le compresseur reçoit un signal plus propre et mieux équilibré
- La compression répond à la *performance musicale*, pas aux artefacts fréquentiels
- Résultat : une compression plus naturelle et transparente

**Quand l'utiliser :**
- Quand la voix présente des problèmes fréquentiels notables (proximité, résonances de la pièce, dureté)
- Quand on veut que le compresseur réponde à la dynamique, pas aux pics de fréquence
- Quand la qualité d'enregistrement est variable

**C'est généralement le choix le plus sûr par défaut** — corrigez les problèmes fréquentiels avant de demander au compresseur de gérer la dynamique.

---

## 4. Le sandwich : EQ→Comp→EQ

```
Voix → [EQ corrective] → [Compresseur] → [EQ tonale] → Bus de mixage
```

C'est le standard professionnel, et pour de bonnes raisons :

1. **Premier EQ (correctif) :** Filtre passe-haut à 80-100 Hz, coupe dans le grave boueux à 200-300 Hz, encoche sur les résonances de la pièce. C'est chirurgical — on supprime les problèmes, on ne façonne pas le timbre.

2. **Compresseur :** Réagit désormais à un signal propre. Réglez le ratio (3:1 à 4:1 typique pour les voix), le seuil pour obtenir environ 6 dB de réduction de gain, une attaque moyenne (10-30 ms) pour préserver les transitoires, un relâchement moyen (50-100 ms).

3. **Second EQ (tonal) :** Façonnez le son de manière créative. Ajoutez de l'air à 10-12 kHz, de la présence à 3-5 kHz, de la chaleur dans les bas-médiums. Cet EQ est placé après la compression, donc vos ajouts ne déclencheront pas le compresseur.

**Pourquoi ça fonctionne :** Séparation des préoccupations. L'EQ corrective prévient les artefacts du compresseur. Le compresseur gère la dynamique sur un signal propre. L'EQ tonale façonne le caractère final sans affecter la dynamique.

---

## 5. Artefacts dépendants de la fréquence à surveiller

| Problème | Cause | Solution |
|----------|-------|----------|
| Pompage sur les plosives | Explosions basse fréquence déclenchant le compresseur | Filtre passe-haut avant le compresseur (EQ→Comp) |
| Sibilance amplifiée | Le compresseur réduit le corps, la sibilance reste | De-esseur avant le compresseur, ou coupe EQ à 6 kHz d'abord |
| Son terne après compression | Attaque rapide écrasant les transitoires | Attaque lente (15-30 ms), ou compression parallèle |
| Timbre incohérent | Le compresseur réagit différemment aux passages calmes et forts | Utiliser 2 étages de compression douce au lieu d'un seul étage fort |

---

## 6. EQ dynamique : l'alternative moderne

L'EQ dynamique combine égalisation et compression en un seul processeur. Chaque bande d'EQ ne s'active que lorsque la fréquence dépasse un seuil — comme un compresseur qui ne travaille que sur des fréquences spécifiques.

**Cas d'usage :** La sibilance qui varie tout au long de l'interprétation. Une coupe statique à 6 kHz ternirait l'ensemble de la voix, mais une coupe en EQ dynamique ne s'active que lorsque la sibilance dépasse le seuil.

Cela ne remplace pas la question Comp→EQ — c'est un outil spécialisé pour les problèmes de dynamique dépendants de la fréquence.

---

## Exercice pratique

### Exercice 1 : Comparer A/B l'ordre
Prenez un enregistrement vocal. Configurez deux chaînes parallèles :
- Chaîne A : Compresseur (4:1, -6 dB de réduction) → EQ (ajout 3 kHz +3 dB, coupe 250 Hz -4 dB)
- Chaîne B : Même EQ → Même compresseur

Écoutez les deux. Où entendez-vous la différence ? Concentrez-vous sur :
- La cohérence des basses fréquences (gestion de l'effet de proximité)
- Le niveau de sibilance
- Le « naturel » global de la compression

### Exercice 2 : Construire un sandwich
Configurez : Passe-haut à 100 Hz + coupe à 250 Hz → Compresseur (3:1) → Ajout de présence à 4 kHz + air à 12 kHz. Comparez avec une chaîne simple EQ-puis-compression.

---

## Points clés à retenir
- **L'ordre compte** — le compresseur réagit aux fréquences les plus fortes dans le signal d'entrée
- **EQ→Comp est le choix par défaut le plus sûr** — corrigez les problèmes avant la compression pour des résultats plus naturels
- **Le sandwich EQ→Comp→EQ est le standard professionnel** — correctif d'abord, tonal ensuite
- **Il n'y a pas d'ordre universellement « correct »** — cela dépend de l'enregistrement, du genre et de l'intention
- **L'EQ dynamique** est un outil moderne pour les problèmes de dynamique dépendants de la fréquence
- L'objectif est toujours : contrôler la dynamique sans détruire le caractère naturel de l'interprétation

## Lectures complémentaires
- Département de physique : Acoustique — fréquence, amplitude et relations harmoniques
- Département de musique : Comment la perception du timbre affecte les décisions de mixage
- Département d'informatique : Algorithmes de traitement du signal (DSP) derrière l'EQ et la compression
- AES (Audio Engineering Society) : Normes de mesure de la sonie (ITU-R BS.1770)

---
*Produit par le cycle de recherche Seldon audio-engineering-2026-03-23-001 le 2026-03-23.*
*Question de recherche : L'ordre compression-avant-EQ versus EQ-avant-compression produit-il des résultats mesurables différents sur les voix ?*
*Croyance : T (confiance : 0.80)*
