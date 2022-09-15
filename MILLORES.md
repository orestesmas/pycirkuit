# Millores possibles
--------------------

1. Cal crear una classe que controli el fitxer que s'està editant en aquest moment (podran haver-n'hi diversos), amb atributs com ara:
    * Nom del fitxer, si se n'hi ha donat algun
    * Directori d'on s'ha carregat
    * Directori on s'ha desat en darrer lloc
    * Tipus de fitxer font (Circuit-Macros, PIC, LaTeX...)
    * La classe pot interpretar els "Magic Comments" en carregar el fitxer per primer cop i activar el ressaltat de sintaxi que convingui.
    * La classe pot registrar en alguna banda el tipus de fitxer font que és capaç d'obrir, proveïnt una o més extensions, i una cadena que identifiqui el tipus. Això es pot usar com a filtre de noms quan es creen els diàlegs d'obertura de fitxer.

1. La lògica rere els load/save i la persistència dels path d'origen i destí és totalment caòtica i feta a base de pedaços. Cal reescriure-la tota.
    
1. Les funcions a baix nivell han de capturar les excepcions? O ho han de fer les de més alt nivell per poder decidir millor? Han de presentar message boxes? Si ho fan, ho haurien de fer totes. Ara hi ha incongruències complicades de mantenir.
    * L'estil de programació [EAFP](https://docs.python.org/2/glossary.html#term-eafp) suggereix tirar pel dret i recollir les excepcions en lloc d'usar if-then per mirar primer si la cosa va bé o no. Barrejar estils no és massa bo.
    * [Aquí](https://code.tutsplus.com/tutorials/professional-error-handling-with-python--cms-25950) diu que hi ha 3 maneres de gestionar les excepcions:
        * Swallow it quietly (Catch -> Handle).
        * Do something like logging, but re-raise the same exception to let higher levels handle (Catch -> Rethrow).
        * Raise a different exception instead of the original.
        
1. Valorar si seria útil una màquina d'estats per tenir cura dels estats del processament.

1. Caldria separar la lògica del processament de la de presentació. Tal vegada el millor seria pensar la lògica del processament des del punt de vista de la CLI, i adaptar-ho després.
    1. Se m'acut definir una classe "pipeline" formada per  diversos passos (ProcessingStep).
    1. En cada pas s'executa algun codi específic. Probablement el més comú serà processar algun fitxer d'entrada per donar una sortida, però pot haver-hi diferents tipus de processament que ara no se m'acuden.
    1. Abans i després de cada pas es poden emetre senyals per tal de donar l'oportunitat a altres coses de posar-hi cullerada.

1. Pensar com hauria de ser i què hauria de tenir un sistema de plugins. Ja n'hi ha alguns de creats:

    * [Yapsy](http://yapsy.sourceforge.net/)
    * [PluginBase](https://github.com/mitsuhiko/pluginbase)
    * [Apispec](https://alysivji.github.io/simple-plugin-system.html)

1. La generació de SVG no es pot deixar en mans del dpic, sinó que s'ha de fer a partir del PDF amb l'eina "pdf2svg" (nova dependència)

