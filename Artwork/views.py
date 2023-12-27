from .forms import *
from .models import *
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail


def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Make sure 'index' is the name of the URL pattern for your index view
            return redirect('index')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'Artwork/signin.html')


def signout(request):
    logout(request)
    return redirect('signin')


def register(request):
    return render(request, "Artwork/register.html")


@login_required(login_url="signin")
def index(request):
    artworks = Artwork.objects.all()
    profile = None
    if request.user.is_authenticated:  # Checks if a user is logged in
        try:
            # Looks up the profile for the logged-in user
            profile = Profile.objects.get(user=request.user)
        except Profile.DoesNotExist:
            messages.error(
                request, "Profile does not exist for the logged in user.")
    context = {
        "artworks": artworks,
        "profile": profile
    }
    return render(request, 'Artwork/index.html', context)


@login_required(login_url="signin")
def create(request):
    if request.method == "POST":
        form = ArtworkForm(request.POST)
        if form.is_valid():
            artwork = form.save(commit=False)
            artwork.instructor = request.user.profile
            artwork.save()
            messages.add_message(
                request, messages.INFO, "Artwork Created successfully . "
            )
            return redirect('index')
    else:
        form = ArtworkForm()

    return render(request, "Artwork/create.html", {"form": form})


@login_required(login_url="signin")
def edit(request, id):
    artwork = get_object_or_404(Artwork, pk=id)

    if request.method == "POST":
        form = ArtworkForm(request.POST, instance=artwork)
        if form.is_valid():
            form.save()
            return redirect('detail', id=id)
    else:
        form = ArtworkForm(instance=artwork)

    context = {
        'form': form,
        'artwork': artwork
    }

    return render(request, 'Artwork/edit.html', context)


@login_required(login_url="signin")
def detail(request, id):
    artwork = get_object_or_404(Artwork, pk=id)
    context = {
        'artwork': artwork,
    }
    return render(request, 'Artwork/detail.html', context)


@login_required(login_url="signin")
def demande(request):
    if request.method == 'POST':
        form = DemandeForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save()
            # Get the values from the form instance
            DateDebut = instance.date_debut
            HDebut = instance.h_debut.strftime('%H:%M')
            DateFin = instance.date_fin
            HFin = instance.h_fin.strftime('%H:%M')
            artwork_obj = instance.artwork
            acquereur_id = instance.acquereur

            formatted_message = f"""
                <p><strong>Date Debut :</strong> {DateDebut}</p>
                <p><strong>Heure Debut :</strong> {HDebut}</p>
                <p><strong>Date Fin :</strong> {DateFin}</p>
                <p><strong>Heure Fin :</strong> {HFin}</p>
                <br />
                <p><strong>Objet :</strong>Demande Artwork {artwork_obj.title}</p>
                <br />
                Monsieur : <strong> {acquereur_id} </strong>
                <br />
                <p><strong>Message :</strong></p>
                <p>
                J'aimerais vous demander si vous seriez d'accord pour prêter votre œuvre "{artwork_obj.title}" Durant la date : {DateDebut} {HDebut} jusqu'a {DateFin} {HFin}.
                </p>
                <br />
                Cordialement,
                <br /><br />
                
                <div style="font-family: Arial, sans-serif; color: #535353; font-size: 10pt;">
                    <p style="color: #2d4e77; font-weight: bold;">
                        PORTAIL Owner
                    </p>

                    <table style="border-collapse: collapse; width: 100%;">
                        <tr>
                            <td style="width: 225px; padding: 0 5.4pt;" valign="top">
                                <img width="154" height="43" src="http://s278824855.onlinehome.fr/images/logo.png" style="display: block;">
                            </td>
                            <td style="width: 413px; padding: 0 5.4pt;" valign="top">
                                <p style="font-weight: bold; color: #092800; line-height: 12.75pt;">
                                    INTELLCAP.
                                </p>
                                <p style="font-size: 8pt; font-weight: bold; color: #092800; line-height: 12.75pt;">
                                    Filiale de INTELLCAP PLC
                                </p>
                                <p style="font-size: 8.5pt; line-height: 12.75pt;">
                                    Hay Jedid | Rue Principale RN | 70050 Rabat 
                                </p>
                                <p style="font-size: 8.5pt; line-height: 12.75pt;">
                                    Mob 212 (0) xxx xxx xxx
                                </p>
                            </td>
                        </tr>
                    </table>

                    <p style="color: #1f497d; text-align: justify; line-height: 1.5;">
                        Cette communication et les pièces jointes sont destinées à la personne ou l'entité nommée ci-dessus et peuvent contenir des éléments confidentiels et / ou privilégiés. Toute révision, divulgation, diffusion, retransmission, publication ou toute autre utilisation ou prise de toute action sur la base de ces informations par des personnes ou entités autres que le destinataire est interdite. Si vous l'avez reçu par erreur, veuillez en informer 
                        l'expéditeur en répondant à cet e-mail ou par téléphone au +212 (0) 662 110 412 et enlevez le matériel de votre système. Les actions de INTELLCAP. et de ses employés sont régies par son code de conduite de manière éthique et en conformité avec toutes les lois anti-corruption et autres lois de chaque endroit où il est présent et en situation irrégulière doit être signalée sur le 
                        <a href="http://s278824855.onlinehome.fr/" target="_blank" style="color: #0056d6;">site web de la société</a> en toute confidentialité. INTELLCAP. est filiale de INTELLCAP Plc. INTELLCAP. au capital de 50 000 000 DH, RC Rabat N°18909, ICE N° 000333383000065 Patente N° 77612500, IF N° 18773131, Site aÌ Hay Jedid, Rue Principale SN - Rabat.
                    </p>

                    <p>
                        <a href="http://s278824855.onlinehome.fr/" target="_blank" style="color: #1f497d;">www.Intellcap.ma</a>
                    </p>
                    <p style="color: #00b050;">
                        Pensez à l'environnement avant d'imprimer cet e-mail.
                    </p>
                </div>

        """
            send_mail(
                'Demande Artwork',
                '',
                acquereur_id.email,
                ['imanejadid16@gmail.com', 'nisrine.rane@usmba.ac.ma',
                    'Houss.benhassoun.1999@gmail.com'],
                html_message=formatted_message,
            )

            return redirect('index')
    else:
        form = DemandeForm()

    return render(request, 'Artwork/demande.html', {'form': form})
