PGDMP     -    /                z            Bibliotheque    14.1    14.1     ?           0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                      false            ?           0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                      false            ?           0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                      false            ?           1262    24588    Bibliotheque    DATABASE     j   CREATE DATABASE "Bibliotheque" WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE = 'French_France.1252';
    DROP DATABASE "Bibliotheque";
                postgres    false            ?            1259    41059 	   categorie    TABLE     g   CREATE TABLE public.categorie (
    id_cat integer NOT NULL,
    libelle_cat character varying(200)
);
    DROP TABLE public.categorie;
       public         heap    postgres    false            ?            1259    41058    categorie_id_cat_seq    SEQUENCE     ?   CREATE SEQUENCE public.categorie_id_cat_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 +   DROP SEQUENCE public.categorie_id_cat_seq;
       public          postgres    false    210            ?           0    0    categorie_id_cat_seq    SEQUENCE OWNED BY     M   ALTER SEQUENCE public.categorie_id_cat_seq OWNED BY public.categorie.id_cat;
          public          postgres    false    209            ?            1259    41066    livres    TABLE       CREATE TABLE public.livres (
    id integer NOT NULL,
    isnb character varying(10) NOT NULL,
    titre character varying(200) NOT NULL,
    nom_aut character varying(50),
    date_pub date,
    editeur character varying(60) NOT NULL,
    categorie_id integer NOT NULL
);
    DROP TABLE public.livres;
       public         heap    postgres    false            ?            1259    41065    livres_id_seq    SEQUENCE     ?   CREATE SEQUENCE public.livres_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 $   DROP SEQUENCE public.livres_id_seq;
       public          postgres    false    212            ?           0    0    livres_id_seq    SEQUENCE OWNED BY     ?   ALTER SEQUENCE public.livres_id_seq OWNED BY public.livres.id;
          public          postgres    false    211            a           2604    41062    categorie id_cat    DEFAULT     t   ALTER TABLE ONLY public.categorie ALTER COLUMN id_cat SET DEFAULT nextval('public.categorie_id_cat_seq'::regclass);
 ?   ALTER TABLE public.categorie ALTER COLUMN id_cat DROP DEFAULT;
       public          postgres    false    209    210    210            b           2604    41069 	   livres id    DEFAULT     f   ALTER TABLE ONLY public.livres ALTER COLUMN id SET DEFAULT nextval('public.livres_id_seq'::regclass);
 8   ALTER TABLE public.livres ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    211    212    212            ?          0    41059 	   categorie 
   TABLE DATA           8   COPY public.categorie (id_cat, libelle_cat) FROM stdin;
    public          postgres    false    210   
       ?          0    41066    livres 
   TABLE DATA           [   COPY public.livres (id, isnb, titre, nom_aut, date_pub, editeur, categorie_id) FROM stdin;
    public          postgres    false    212   ?       ?           0    0    categorie_id_cat_seq    SEQUENCE SET     C   SELECT pg_catalog.setval('public.categorie_id_cat_seq', 10, true);
          public          postgres    false    209                        0    0    livres_id_seq    SEQUENCE SET     <   SELECT pg_catalog.setval('public.livres_id_seq', 10, true);
          public          postgres    false    211            d           2606    41064    categorie categorie_pkey 
   CONSTRAINT     Z   ALTER TABLE ONLY public.categorie
    ADD CONSTRAINT categorie_pkey PRIMARY KEY (id_cat);
 B   ALTER TABLE ONLY public.categorie DROP CONSTRAINT categorie_pkey;
       public            postgres    false    210            f           2606    41071    livres livres_pkey 
   CONSTRAINT     P   ALTER TABLE ONLY public.livres
    ADD CONSTRAINT livres_pkey PRIMARY KEY (id);
 <   ALTER TABLE ONLY public.livres DROP CONSTRAINT livres_pkey;
       public            postgres    false    212            g           2606    41072    livres livres_categorie_id_fkey    FK CONSTRAINT     ?   ALTER TABLE ONLY public.livres
    ADD CONSTRAINT livres_categorie_id_fkey FOREIGN KEY (categorie_id) REFERENCES public.categorie(id_cat);
 I   ALTER TABLE ONLY public.livres DROP CONSTRAINT livres_categorie_id_fkey;
       public          postgres    false    212    210    3172            ?   ?   x?5?;?1???=?)`䱰#K?P?6)M???98'???і??#X??b5?UrT\??~???1????ܹi??&?	l*7E8?=??ʷg?3????9?f??C???W????9??_c)??
.a?jw
?E??eS
8?!i??-g??L.??p蘤kgM;???4@?ܶP?      ?   a  x?M?KN?0???)?bW4S??v,`??X?1?;?H???#??s??2\?????"E??G???v	TtEU?p??(??%??aI*\?N?<?????V?rR??ds?8G񌵤L!3L?TE*?????ؓ6$V,?|??????mE?ጲ?Ui???	?);n?W???(??;
+V??P?c쬨%ۭ??pN?%/?w??y????? ??k????jPs???K?d??T-{\R?p2u??(???7???Yz?-c???V??????8???_e??P?[??)?2?hA֖Ԇ?0g???[?1?uޒ?ja?]7????}?)ۘ??8al??.??s?G?????w????}???     