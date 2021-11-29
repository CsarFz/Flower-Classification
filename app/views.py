from flask import Blueprint, render_template, request, redirect, url_for
from flask.helpers import flash
from flask_login import login_required, current_user
from .models import Flower, User
import tensorflow as tf
from werkzeug.utils import secure_filename
import os
import numpy as np
from . import db

views = Blueprint("views", __name__)
model = tf.keras.models.load_model("deteccion_petalos.h5")
classes = [
    'pink primrose',
    'hard-leaved pocket orchid',
    'canterbury bells',
    'sweet pea',
    'wild geranium',
    'tiger lily',
    'moon orchid',
    'bird of paradise',
    'monkshood',
    'globe thistle',  # 00 - 09
    'snapdragon',
    "colt's foot",
    'king protea',
    'spear thistle',
    'yellow iris',
    'globe-flower',
    'purple coneflower',
    'peruvian lily',
    'balloon flower',
    'giant white arum lily',  # 10 - 19
    'fire lily',
    'pincushion flower',
    'fritillary',
    'red ginger',
    'grape hyacinth',
    'corn poppy',
    'prince of wales feathers',
    'stemless gentian',
    'artichoke',
    'sweet william',  # 20 - 29
    'carnation',
    'garden phlox',
    'love in the mist',
    'cosmos',
    'alpine sea holly',
    'ruby-lipped cattleya',
    'cape flower',
    'great masterwort',
    'siam tulip',
    'lenten rose',  # 30 - 39
    'barberton daisy',
    'daffodil',
    'sword lily',
    'poinsettia',
    'bolero deep blue',
    'wallflower',
    'marigold',
    'buttercup',
    'daisy',
    'common dandelion',  # 40 - 49
    'petunia',
    'wild pansy',
    'primula',
    'sunflower',
    'lilac hibiscus',
    'bishop of llandaff',
    'gaura',
    'geranium',
    'orange dahlia',
    'pink-yellow dahlia',  # 50 - 59
    'cautleya spicata',
    'japanese anemone',
    'black-eyed susan',
    'silverbush',
    'californian poppy',
    'osteospermum',
    'spring crocus',
    'iris',
    'windflower',
    'tree poppy',  # 60 - 69
    'gazania',
    'azalea',
    'water lily',
    'rose',
    'thorn apple',
    'morning glory',
    'passion flower',
    'lotus',
    'toad lily',
    'anthurium',  # 70 - 79
    'frangipani',
    'clematis',
    'hibiscus',
    'columbine',
    'desert-rose',
    'tree mallow',
    'magnolia',
    'cyclamen ',
    'watercress',
    'canna lily',  # 80 - 89
    'hippeastrum ',
    'bee balm',
    'pink quill',
    'foxglove',
    'bougainvillea',
    'camellia',
    'mallow',
    'mexican petunia',
    'bromelia',
    'blanket flower',  # 90 - 99
    'trumpet creeper',
    'blackberry lily',
    'common tulip',
    'wild rose'
]


@views.route("/")
@views.route("/home")
def home():
    return render_template("index.html", user=current_user)


@views.route("/login")
def login():
    if current_user.is_authenticated:
        return redirect(url_for("views.home"))
    else:
        return render_template("login.html", user=current_user)


@views.route("/sign-up")
def sign_up():
    if current_user.is_authenticated:
        return redirect(url_for("views.home"))
    else:
        return render_template("signup.html", user=current_user)


@views.route("/what-flower-is-it")
@login_required
def what_flower_is_it():
    return render_template("what-flower-is-it.html", user=current_user)


@views.route("/profile")
@login_required
def profile():
    user = User.query.filter_by(username=current_user.username).first()

    if not user:
        flash('No existe el usuario.', category='error')
        return redirect(url_for('views.login'))

    flowers = user.flowers
    return render_template("profile.html", user=current_user, flower_len=len(flowers))


@views.route("/myflowers")
@login_required
def myflowers():
    user = User.query.filter_by(username=current_user.username).first()

    if not user:
        flash('No existe el usuario.', category='error')
        return redirect(url_for('views.login'))

    flowers = user.flowers

    return render_template("myflowers.html",
                        user=current_user,
                        flowers=flowers,
                        flower_len=len(flowers))


@views.route("/classify-flower", methods=["GET", "POST"])
@login_required
def classify_flower():
    if request.method == "POST":
        if request.files:
            image = request.files["image"]

            if not image.filename == "":
                filename = secure_filename(image.filename)

                path = os.path.join(
                    os.path.dirname(os.path.realpath(__file__)),
                    'static/assets/img/flowers', filename)
                image.save(path)

                # Imagen a Tensorflow
                imagen_externa = tf.keras.preprocessing.image.load_img(path)
                matriz_imag_ext = tf.keras.preprocessing.image.img_to_array(
                    imagen_externa)

                # Cambiar el tamaño de la imagen
                matriz_imag_ext = tf.image.resize(matriz_imag_ext, [512, 512])

                # Normalizar la imagen
                matriz_imag_ext = matriz_imag_ext / 255

                # Predicción de la imagen cargada al modelo ya entrenado
                prediccion = model.predict(np.array([matriz_imag_ext]))

                argument = np.argmax(prediccion[0])
                class_ = classes[np.argmax(prediccion[0])]
                path = path.split(os.path.dirname(os.path.realpath(__file__)))

                flower = Flower(name=class_,
                                user_id=current_user.id,
                                path=path[1])
                db.session.add(flower)
                db.session.commit()

                return render_template("flower.html",
                                        user=current_user,
                                        clase=class_,
                                        path=path[1],
                                        argument=argument)
            else:
                flash("Por favor seleccione una imagen.", category="error")
                return redirect(url_for('views.home'))