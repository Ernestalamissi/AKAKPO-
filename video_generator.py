#08/07/08/2025 Ernest avec vidéo libre d'auteur
import os
import atexit
import shutil
import asyncio
import edge_tts
import subprocess
import numpy as np
import nest_asyncio
from mutagen.mp3 import MP3
from moviepy.editor import (
    ImageClip, concatenate_videoclips, CompositeVideoClip, 
TextClip,concatenate_audioclips,
    AudioFileClip, CompositeAudioClip, VideoFileClip,vfx
)
from PIL import Image, ImageFilter
import tempfile

# Patch pour compatibilité Pillow récente
if not hasattr(Image, 'ANTIALIAS'):
    Image.ANTIALIAS = Image.Resampling.LANCZOS

# === Texte découpé par partie ===

#Citron à jeun après 60 ans : 5 bienfaits majeurs et 3 erreurs dangereuses 

phrases = [
    """
Le citron, ce petit fruit jaune que nous voyons tous les jours, cache en 
réalité des secrets puissants pour votre santé. Mais attention : mal 
l’utiliser peut parfois faire plus de mal que de bien.

Chaque matin, des milliers de personnes – surtout après 50 ans – 
commencent leur journée par un verre d’eau tiède citronnée. Et ce n’est 
pas un hasard : ce rituel, validé par de nombreuses études scientifiques, 
améliore la digestion, renforce les défenses immunitaires et aide même à 
garder une peau éclatante.

Cependant, malgré ses incroyables bienfaits, 3 erreurs très courantes 
peuvent totalement annuler ses effets… voire nuire à votre santé !
Restez jusqu’à la fin, car je vais aussi vous révéler les 3 aliments qui 
décuplent la puissance du citron.

Avant de commencer, dites-nous en commentaire : quel est votre rituel 
santé préféré le matin ? Et surtout, abonnez-vous pour recevoir chaque 
semaine des conseils simples, naturels et efficaces pour rester en pleine 
forme.
    """,

    """
Pourquoi boire de l’eau citronnée à jeun ? Voici 5 bienfaits prouvés par 
la science :

1 – Un soutien naturel pour le foie et la digestion.
Pendant que vous dormez, votre foie travaille sans relâche : il filtre 
votre sang, élimine les toxines et décompose les déchets. Mais au réveil, 
il a besoin d’un coup de pouce pour redémarrer efficacement.

Le citron est parfait pour ça : son acide citrique stimule la production 
de bile, essentielle pour bien digérer les graisses. Il contient aussi des 
antioxydants puissants – comme l’hespéridine et la diosmine – qui 
protègent les cellules du foie contre les radicaux libres.

Certaines études montrent qu’un verre d’eau citronnée à jeun pourrait 
améliorer la fonction hépatique de près de 25 % chez les plus de 60 ans.
En bonus, cette boisson favorise le péristaltisme intestinal, ce qui aide 
en cas de digestion lente ou de constipation.
    """,

    """
2 – Renforcement naturel de l’immunité.
Avec l’âge, notre système immunitaire s’affaiblit – un phénomène appelé 
immunosénescence. Résultat : nous devenons plus vulnérables aux 
infections.

Le citron, riche en vitamine C, agit comme un véritable bouclier naturel 
en stimulant la production de globules blancs, les cellules qui nous 
défendent contre les virus et bactéries.

Boire de l’eau citronnée à jeun améliore l’absorption de cette vitamine, 
car l’estomac est vide. En plus, le citron contient du limonène, un 
puissant antiviral et antimicrobien.
Résultat ? Une réduction possible de 40 % des infections respiratoires 
chez les personnes âgées, selon certaines études.
    """,

    """
3 – Équilibre du pH et protection contre l’ostéoporose.
Même si le citron a un goût acide, une fois métabolisé, il devient 
alcalinisant et aide à maintenir un pH sanguin stable.

Un organisme trop acide va puiser dans le calcium des os pour se réguler, 
ce qui fragilise la masse osseuse et augmente le risque d’ostéoporose.
Boire un verre d’eau citronnée chaque matin est donc une arme simple mais 
efficace pour garder des os solides et en bonne santé.
    """,

    """
4 – Booster l’absorption du fer et prévenir l’anémie.
Une personne sur cinq après 60 ans souffre d’anémie sans même le savoir. 
La vitamine C du citron transforme le fer végétal peu assimilable (présent 
dans les lentilles, épinards, etc.) en une forme que notre corps absorbe 
beaucoup mieux.

Résultat ? Jusqu’à 5 fois plus de fer est absorbé si vous buvez un verre 
d’eau citronnée avant un petit-déjeuner riche en fer.
    """,

    """
5 – Réhydratation et protection des reins.
Avec l’âge, la sensation de soif diminue et les reins filtrent moins bien. 
Cela peut entraîner une déshydratation, des infections urinaires, et même 
des troubles de la mémoire.

Un simple verre d’eau tiède citronnée le matin réhydrate l’organisme, 
stimule les reins et favorise l’élimination des toxines. L’acide citrique 
agit comme un diurétique doux sans provoquer de déshydratation.
    """,

    """
Les 3 erreurs à éviter absolument après l’eau citronnée :

1 – Le café tout de suite après.
Le combo citron + café est trop agressif pour l’estomac. Le citron 
augmente l’acidité, et le café en rajoute une couche. Résultat : brûlures, 
reflux, voire gastrite.
En plus, les tanins du café réduisent l’absorption de la vitamine C.
Astuce : attendez 45 min à 1 heure avant de prendre votre café.
    """,

    """
2 – Les produits laitiers.
Le citron fait cailler les protéines du lait, ce qui ralentit la digestion 
et provoque ballonnements ou douleurs. Le calcium du lait bloque aussi 
l’action de la vitamine C.
Astuce : attendez 2 heures avant de consommer du lait ou optez pour des 
alternatives végétales (amande, avoine, coco).
    """,

    """
3 – Certains médicaments.
Les antibiotiques (quinolones, tétracyclines), les antiacides et les 
traitements contre l’ostéoporose peuvent être moins efficaces si vous les 
prenez juste après l’eau citronnée.
Astuce : espacez la prise de 1 à 2 heures et demandez l’avis de votre 
médecin.
    """,

    """
Les 3 aliments qui boostent l’effet du citron :

1 – L’avoine complète.
Riche en fibres et bêta-glucanes, elle stabilise la glycémie et soutient 
le cœur.
Astuce : un porridge à l’avoine, fruits rouges et cannelle, c’est le 
petit-déj parfait.
    """,

    """
2 – Papaye & goyave.
Ultra riches en vitamine C et en enzymes digestives, elles favorisent la 
digestion et l’absorption du fer.
Astuce : une salade papaye-goyave-gingembre 1 heure après l’eau citronnée.
    """,

    """
3 – Légumes verts à feuilles.
Épinards, kale ou bette à carde : parfaits pour le fer, la vision et la 
circulation sanguine.
Astuce : un smoothie vert ou une omelette aux épinards = combo gagnant !
    """,

    """
Conseils pratiques :
- Eau tiède entre 37 et 40°C (jamais bouillante).
- ½ citron pressé dans 250 ml d’eau filtrée.
- Attendre 15 à 20 min avant de manger.
- Utiliser une paille si vous avez les dents sensibles.
- Privilégier les citrons bio, surtout si vous mettez un peu de zeste.

Cas particuliers :
- Maladies rénales ou cardiaques : demandez conseil à votre médecin.
- Reflux ou allergies : adaptez la dose.
    """,

    """
Conclusion :
Boire un verre d’eau tiède citronnée chaque matin est une habitude simple, 
naturelle et incroyablement efficace après 50 ou 60 ans. Mais pour en 
profiter pleinement, évitez les mauvaises associations et combinez-la aux 
bons aliments.

Et vous, avez-vous déjà essayé ce rituel ? Quels changements avez-vous 
remarqués ?
Partagez vos expériences dans les commentaires !
Et surtout, abonnez-vous et activez la cloche pour recevoir chaque semaine 
nos meilleurs conseils santé et bien-être.
    """
]

video_libre = [
    "/Users/user/Desktop/DonnerIA/video/Eau_citronner.mp4",
    "/Users/user/Desktop/DonnerIA/video/intestin_constipation.mp4",
    "/Users/user/Desktop/DonnerIA/video/immunite_diseases.mp4",
    "/Users/user/Desktop/DonnerIA/video/musclehumain.mp4",
    "/Users/user/Desktop/DonnerIA/video/anemie.mp4",
    "/Users/user/Desktop/DonnerIA/video/rein_testoterole.mp4",
    "/Users/user/Desktop/DonnerIA/video/boire_cafe.mp4",
    "/Users/user/Desktop/DonnerIA/video/produit_laitier.mp4",
    "/Users/user/Desktop/DonnerIA/video/prendre_medicament.mp4",
    "/Users/user/Desktop/DonnerIA/video/avoine.mp4",
    "/Users/user/Desktop/DonnerIA/video/papaya_breakfast.mp4",
    "/Users/user/Desktop/DonnerIA/video/epinard.mp4",
    "/Users/user/Desktop/DonnerIA/video/couper_eau_tiede.mp4",
    "/Users/user/Desktop/DonnerIA/video/robo_bois_eau.mp4"
]

# ===  PARAMÈTRES ===
logo_path = "/Users/user/Desktop/DonnerIA/logoLesBienfaitsAliments.jpg"
bg_music_path = "/Users/user/Desktop/DonnerIA/musiqueFond.mp3"
output_path = "/Users/user/Desktop/DonneeIA/eau_citronner.mp4"
temp_dir = "/Users/user/Desktop/DonneeIA/audio_temp"
video_robot_path = "/Users/user/Desktop/DonnerIA/docteurs.mp4"

# ========== Synthèse vocale ==========
nest_asyncio.apply()

async def synthese_voix(texte, fichier_audio, voix="fr-FR-HenriNeural"):
    communicate = edge_tts.Communicate(text=texte, voice=voix)
    await communicate.save(fichier_audio)

# ========== Fonctions visuelles ==========
def get_logo(duration):
    return (
        ImageClip(logo_path)
        .set_duration(duration)
        .resize(height=250)
        .set_position(("right", "top"))
                
    )
#.margin(right=10, top=10, opacity=0)

def pulsation(t):
    return 1 + 0.05 * np.sin(2 * np.pi * t * 1.5)

def bouton_abonne(dur):
    return (
        TextClip("👍 Abonne-toi", fontsize=60, color='white', 
bg_color='red', font="Arial-Bold")
        .set_duration(dur)
        .set_position(("center", 1100))
        .resize(pulsation)        
    )
def dynamics_video(audio_file, video_path_libre,duration_total,video_robot_path=video_robot_path):
    duration_robot = int(duration_total * 0.25)  # 25% du temps pour le robot
    duration_libbre = duration_total - duration_robot
    def video_robot(video_robot_path, dur_audio):
        video = VideoFileClip(video_robot_path).without_audio()
        n_repeats = int(dur_audio // video.duration) + 1
        video_looped = concatenate_videoclips([video] * n_repeats).subclip(0, dur_audio)
        video_looped = video_looped.resize((1920, 1080))
        return video_looped
    def video_libre(video_path, dur_audio):
        video = VideoFileClip(video_path).without_audio()
        if video.duration >= dur_audio:
            # Couper la vidéo à la durée de l'audio
            video_final = video.subclip(0, dur_audio)
        else: 
            # Répéter la vidéo jusqu'à couvrir la durée audio
            n_repeats = int(dur_audio // video.duration) + 1
            video_looped = concatenate_videoclips([video] * n_repeats)
            video_final = video_looped.subclip(0, dur_audio)
        # Optionnel : zoom progressif
        video_final = video_final.resize(lambda t: 1 + 0.02 * t)
        # 🔥 Forcer le format 1920x1080
        video_final = video_final.resize((1920, 1080))
        return video_final    
    # Génération des clips
    wav2lip_clip = video_robot(video_robot_path, duration_robot)  # ➤ robot au début
    clip_animation = video_libre(video_path_libre,duration_libbre)  # ➤ vidéo libre

    # Composition finale : d’abord le robot, puis animation
    final = concatenate_videoclips([wav2lip_clip, clip_animation],method="compose")
    # Reprend l'audio original sur toute la durée
    audio_clip = AudioFileClip(audio_file).set_duration(duration_total)
    final = final.set_audio(audio_clip)
    return final
# ========== Création des clips ==========
clips = []

for i, (text, video_libre_path) in enumerate(zip(phrases, video_libre)):
    os.makedirs(temp_dir, exist_ok=True)
    audio_file = os.path.join(temp_dir, f"audio_{i}.mp3")
    
    asyncio.run(synthese_voix(text, audio_file))
    duree = AudioFileClip(audio_file).duration
    clip = dynamics_video( audio_file, video_libre_path, duree)
    
    overlays = [clip]
    if i == 0 or i == len(phrases) - 1:
        overlays.append(get_logo(duree))
        overlays.append(bouton_abonne(duree))

    final = CompositeVideoClip(overlays, size=(1920,1080))
    
    clips.append(final)    

# ========== Fusion et audio ==========
final_clip = concatenate_videoclips(clips, method="compose")

main_audio = final_clip.audio
bg_music = AudioFileClip(bg_music_path).volumex(0.15)  # Volume ajusté

# Adapter la musique à la durée de la vidéo 
n_repeats = int(main_audio.duration // bg_music.duration) + 1
bg_music_adapter = concatenate_audioclips([bg_music] * n_repeats).subclip(0, main_audio.duration)

# Fusion audio
audio_mix = CompositeAudioClip([main_audio, bg_music_adapter])
final_clip= final_clip.set_audio(audio_mix)#.fadeout(1)  # effet pro


# ========== Export ==========
final_clip.write_videofile(
    output_path,
    codec="libx264",
    audio_codec="aac",
    bitrate="5000k",
    fps=30,
    preset="veryfast",
    threads=os.cpu_count()
)

# ========== Nettoyage ==========
if os.path.exists(temp_dir):
    shutil.rmtree(temp_dir)        
print("✅ Vidéo exportée avec succès et fichiers temporaires supprimés.")

