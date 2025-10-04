const API_BASE = "/api/v1";
const body = document.body;
const pageId = body?.dataset?.page ?? "home";
const notifications = document.querySelector("#notifications");
const localeSwitcher = document.querySelector("#locale-switcher");
const headerLoginButton = document.querySelector("#header-login");
const headerSignupButton = document.querySelector("#header-signup");
const apiBaseLabel = document.querySelector("#api-base");

if (apiBaseLabel) {
  apiBaseLabel.textContent = API_BASE;
}

function notify(type, message) {
  if (!notifications) {
    return;
  }
  const toast = document.createElement("div");
  toast.className = `toast ${type}`;
  toast.textContent = message;
  notifications.appendChild(toast);
  setTimeout(() => {
    toast.classList.add("fade");
    toast.addEventListener(
      "transitionend",
      () => toast.remove(),
      { once: true }
    );
    toast.style.opacity = "0";
  }, 3500);
}

async function request(path, options = {}) {
  const response = await fetch(`${API_BASE}${path}`, {
    headers: {
      "Content-Type": "application/json",
      ...(options.headers || {}),
    },
    ...options,
  });

  if (!response.ok) {
    let detail = null;
    try {
      detail = await response.json();
    } catch (error) {
      detail = null;
    }
    const error = new Error(detail?.detail || response.statusText || "Request failed");
    error.status = response.status;
    error.payload = detail;
    throw error;
  }

  if (response.status === 204) {
    return null;
  }

  try {
    return await response.json();
  } catch (error) {
    return null;
  }
}

const translations = {
  en: {
    "badge.beta": "Beta",
    "nav.home": "Home",
    "nav.profiles": "Profiles",
    "nav.events": "Events",
    "nav.rosters": "Rosters",
    "nav.federations": "Federations",
    "nav.about": "About",
    "locale.label": "Choose language",
    "action.login": "Log in",
    "action.signup": "Create account",
    "footer.powered": "Trackeo · Powered by FastAPI · API base:",
    "footer.location": "Headquartered in Atlanta, GA · Scaling across South America with localized partners.",
    "hero.eyebrow": "Latin American Athletics Intelligence",
    "hero.title": "Trackeo connects federations, coaches, and fans across the Americas.",
    "hero.description": "Explore verified performances, multilingual news, and premium insights that highlight the rise of track & field from São Paulo to Bogotá. Built in Atlanta for the continent.",
    "hero.explore": "Explore as guest",
    "hero.subscribe": "View coach plans",
    "preview.title": "Regional spotlight",
    "preview.subtitle": "19 federations streaming live splits and heat sheets.",
    "preview.metric_meets": "Verified meets",
    "preview.metric_athletes": "Athletes tracked",
    "preview.metric_rosters": "Roster updates",
    "search.title": "Search Trackeo's universe",
    "search.subtitle": "Find athletes, events, rosters, and bilingual news in one place.",
    "search.placeholder": "Search for an athlete, club, or meet",
    "search.aria": "Search Trackeo",
    "search.filters": "Search categories",
    "search.filter_all": "All",
    "search.filter_athletes": "Athletes",
    "search.filter_events": "Events",
    "search.filter_rosters": "Rosters",
    "search.filter_news": "News",
    "search.empty": "Start typing to explore Trackeo's data universe.",
    "search.no_results": "No matches yet. Try adjusting your filters or spelling.",
    "home.athletes_title": "Athletes",
    "home.athletes_subtitle": "Browse the roster or showcase a rising star from your federation.",
    "home.athletes_seed": "Reload Sample Athletes",
    "home.athletes_form_title": "Create athlete profile",
    "home.athletes_submit": "Register athlete",
    "home.athletes_empty": "No athletes have been registered yet.",
    "home.athletes_hint": "Use the creation form or load curated sample athletes to populate the roster.",
    "home.events_title": "Events",
    "home.events_subtitle": "Track the latest competitions from Atlanta to Buenos Aires.",
    "home.events_seed": "Reload Sample Events",
    "home.events_form_title": "Schedule a new meet",
    "home.events_submit": "Create event",
    "home.events_empty": "No events have been scheduled yet.",
    "home.events_hint": "Use the meet form or reload the curated calendar of sample events.",
    "home.rosters_title": "Rosters",
    "home.rosters_subtitle": "Keep squads aligned with verified athlete eligibility.",
    "home.rosters_empty": "No rosters available yet.",
    "home.rosters_hint": "Federations upload rosters directly for instant publication.",
    "home.news_title": "News",
    "home.news_subtitle": "Bilingual coverage powered by Trackeo correspondents and partners.",
    "home.news_empty": "No news stories have been published yet.",
    "home.news_hint": "Follow Trackeo Insights for the latest headlines.",
    "premium.title": "Coach & Federation tiers",
    "premium.subtitle": "Unlock deep analytics, heat maps, and race video archives tailored to your role.",
    "premium.compare": "Compare plans",
    "premium.guest_title": "Guest",
    "premium.guest_price": "Free",
    "premium.guest_benefit_1": "Open event calendar",
    "premium.guest_benefit_2": "Headline stats and news highlights",
    "premium.guest_benefit_3": "Regional localization (ES/PT)",
    "premium.premium_title": "Premium",
    "premium.premium_price": "$9 / month",
    "premium.premium_benefit_1": "Full athlete history & season analytics",
    "premium.premium_benefit_2": "Video library with race markers",
    "premium.premium_benefit_3": "Priority support in English & Spanish",
    "premium.coach_title": "Coach",
    "premium.coach_price": "$29 / month",
    "premium.coach_benefit_1": "Roster syncing with federation data",
    "premium.coach_benefit_2": "Practice planning & workload insights",
    "premium.coach_benefit_3": "Invite athletes and manage staff",
    "home.federations_title": "Federations upload securely",
    "home.federations_subtitle": "Trusted partners share verified performances through Trackeo's ingestion APIs.",
    "home.federations_cta": "Submit official results",
    "home.federations_card_1_title": "Verified pipelines",
    "home.federations_card_1_body": "Encrypted submissions with audit trails ensure accuracy before publishing.",
    "home.federations_card_2_title": "Localized infrastructure",
    "home.federations_card_2_body": "Edge nodes in São Paulo, Bogotá, and Santiago reduce upload latency.",
    "home.federations_card_3_title": "Atlanta operations",
    "home.federations_card_3_body": "On-the-ground support from Trackeo HQ keeps every federation onboarding smooth.",
    "form.full_name": "Full name",
    "form.full_name_placeholder": "Jane Runner",
    "form.email": "Email",
    "form.email_placeholder": "you@example.com",
    "form.role": "Role",
    "form.role_placeholder": "athlete",
    "form.password": "Password",
    "form.password_placeholder": "Password123",
    "form.event_name": "Name",
    "form.event_name_placeholder": "Summer Invitational",
    "form.location": "Location",
    "form.location_placeholder": "Lisbon, Portugal",
    "form.start_date": "Start date",
    "form.end_date": "End date",
    "form.federation_id": "Federation ID",
    "form.federation_id_placeholder": "Optional",
    "profiles.title": "Athlete & staff profiles",
    "profiles.subtitle": "Search federated accounts with verified event history and multilingual bios.",
    "profiles.refresh": "Refresh profiles",
    "profiles.create": "Create new profile",
    "profiles.list_title": "Directory",
    "profiles.list_subtitle": "Live data from the Trackeo accounts service.",
    "profiles.filter_placeholder": "Filter by name or email",
    "profiles.filter_aria": "Filter profiles",
    "profiles.empty": "No profiles were found.",
    "profiles.hint": "Adjust your filters or create a new account from the sign-up view.",
    "events.title": "Competition calendar",
    "events.subtitle": "Monitor official meets created by federations and Trackeo partners.",
    "events.create": "Schedule event",
    "events.refresh": "Refresh",
    "events.list_title": "Upcoming & recent meets",
    "events.list_subtitle": "Data is sourced from the events service and updates instantly.",
    "events.filter_upcoming": "Show only upcoming",
    "events.empty": "No events are published yet.",
    "events.hint": "Create a meet or ask your federation to upload an official calendar.",
    "rosters.title": "Federation rosters",
    "rosters.subtitle": "Track eligibility, divisions, and staffing with live updates from the roster service.",
    "rosters.refresh": "Refresh rosters",
    "rosters.list_title": "Latest submissions",
    "rosters.list_subtitle": "Verified rosters arrive through secure federation uploads.",
    "rosters.filter_placeholder": "Filter by club or country",
    "rosters.filter_aria": "Filter rosters",
    "rosters.empty": "No rosters are available yet.",
    "rosters.hint": "Federations can upload a roster file from the secure upload view.",
    "login.title": "Sign in to Trackeo",
    "login.subtitle": "Use your verified email address to access premium federation tools.",
    "login.submit": "Sign in",
    "login.switch": "Need an account?",
    "login.switch_link": "Create one now.",
    "signup.title": "Create your Trackeo account",
    "signup.subtitle": "Join Trackeo to manage rosters, follow events, and unlock analytics.",
    "signup.tier": "Subscription tier",
    "signup.tier_free": "Free",
    "signup.tier_premium": "Premium",
    "signup.tier_coach": "Coach",
    "signup.tier_federation": "Federation",
    "signup.role_fan": "Fan",
    "signup.role_athlete": "Athlete",
    "signup.role_coach": "Coach",
    "signup.role_federation": "Federation",
    "signup.role_scout": "Scout",
    "signup.submit": "Create account",
    "signup.switch": "Already registered?",
    "signup.switch_link": "Sign in.",
    "federations.title": "Secure federation uploads",
    "federations.subtitle": "Submit encrypted result bundles with audit trails and automated verification.",
    "federations.refresh": "Refresh submissions",
    "federations.form_title": "Upload official files",
    "federations.form_subtitle": "Provide a signed storage link. Trackeo validates checksum and processes asynchronously.",
    "federations.token": "Access token",
    "federations.token_placeholder": "Bearer token",
    "federations.name": "Federation name",
    "federations.name_placeholder": "Confederación Sudamericana",
    "federations.email_placeholder": "contact@federation.org",
    "federations.payload": "Secure payload URL",
    "federations.payload_placeholder": "https://storage.example.com/results.json",
    "federations.notes": "Notes (optional)",
    "federations.notes_placeholder": "Describe the event or include validation hints",
    "federations.submit": "Submit for processing",
    "federations.submissions_title": "Submission history",
    "federations.submissions_subtitle": "Track processing, checksum validation, and verification status.",
    "federations.submissions_empty": "No submissions yet. Upload your first official file to begin.",
    "about.title": "About Trackeo",
    "about.subtitle": "Built in Atlanta and powered by federations across Latin America.",
    "about.mission_title": "Mission",
    "about.mission_subtitle": "We amplify athletes with trusted data, multilingual coverage, and equitable access.",
    "about.mission_body_1": "Trackeo centralizes competition data for 19 federations while delivering insights in English, Spanish, and Portuguese.",
    "about.mission_body_2": "Our platform supports coaches with workload analytics, empowers fans with contextual storytelling, and streamlines compliance for federation staff.",
    "about.team_title": "Team & partners",
    "about.team_subtitle": "Trackeo collaborates with local statisticians, journalists, and federations throughout the region.",
    "about.team_item_1_title": "Atlanta HQ",
    "about.team_item_1_body": "Product, engineering, and partnerships operate from Atlanta, coordinating multilingual coverage.",
    "about.team_item_2_title": "Regional bureaus",
    "about.team_item_2_body": "Embedded correspondents in Bogotá, São Paulo, Santiago, and Mexico City file news and verify results.",
    "about.team_item_3_title": "Federation council",
    "about.team_item_3_body": "An advisory council of federation leaders ensures Trackeo meets security and accessibility standards.",
  },
  es: {
    "badge.beta": "Beta",
    "nav.home": "Inicio",
    "nav.profiles": "Perfiles",
    "nav.events": "Eventos",
    "nav.rosters": "Planteles",
    "nav.federations": "Federaciones",
    "nav.about": "Acerca de",
    "locale.label": "Elegir idioma",
    "action.login": "Iniciar sesión",
    "action.signup": "Crear cuenta",
    "footer.powered": "Trackeo · Impulsado por FastAPI · Base del API:",
    "footer.location": "Con sede en Atlanta, GA · Escalando por Sudamérica con socios locales.",
    "hero.eyebrow": "Inteligencia atlética latinoamericana",
    "hero.title": "Trackeo conecta federaciones, entrenadores y aficionados en las Américas.",
    "hero.description": "Explora actuaciones verificadas, noticias multilingües e insights premium que destacan el auge del atletismo de São Paulo a Bogotá. Construido en Atlanta para el continente.",
    "hero.explore": "Explorar como invitado",
    "hero.subscribe": "Ver planes para entrenadores",
    "preview.title": "Enfoque regional",
    "preview.subtitle": "19 federaciones transmitiendo parciales y heat sheets en vivo.",
    "preview.metric_meets": "Competencias verificadas",
    "preview.metric_athletes": "Atletas monitoreados",
    "preview.metric_rosters": "Actualizaciones de planteles",
    "search.title": "Busca en el universo de Trackeo",
    "search.subtitle": "Encuentra atletas, eventos, planteles y noticias bilingües en un solo lugar.",
    "search.placeholder": "Busca un atleta, club o torneo",
    "search.aria": "Buscar en Trackeo",
    "search.filters": "Categorías de búsqueda",
    "search.filter_all": "Todo",
    "search.filter_athletes": "Atletas",
    "search.filter_events": "Eventos",
    "search.filter_rosters": "Planteles",
    "search.filter_news": "Noticias",
    "search.empty": "Comienza a escribir para explorar el universo de datos de Trackeo.",
    "search.no_results": "Sin coincidencias. Ajusta tus filtros o revisa la ortografía.",
    "home.athletes_title": "Atletas",
    "home.athletes_subtitle": "Explora el plantel o destaca a una promesa de tu federación.",
    "home.athletes_seed": "Recargar atletas de ejemplo",
    "home.athletes_form_title": "Crear perfil de atleta",
    "home.athletes_submit": "Registrar atleta",
    "home.athletes_empty": "Aún no se han registrado atletas.",
    "home.athletes_hint": "Usa el formulario o carga atletas de ejemplo para poblar el plantel.",
    "home.events_title": "Eventos",
    "home.events_subtitle": "Sigue las últimas competencias de Atlanta a Buenos Aires.",
    "home.events_seed": "Recargar eventos de ejemplo",
    "home.events_form_title": "Programar un nuevo meeting",
    "home.events_submit": "Crear evento",
    "home.events_empty": "Todavía no hay eventos programados.",
    "home.events_hint": "Usa el formulario o recarga el calendario curado de eventos.",
    "home.rosters_title": "Planteles",
    "home.rosters_subtitle": "Mantén los equipos alineados con elegibilidad verificada.",
    "home.rosters_empty": "Aún no hay planteles disponibles.",
    "home.rosters_hint": "Las federaciones cargan planteles directamente para su publicación instantánea.",
    "home.news_title": "Noticias",
    "home.news_subtitle": "Cobertura bilingüe de corresponsales y socios de Trackeo.",
    "home.news_empty": "Todavía no se han publicado noticias.",
    "home.news_hint": "Sigue a Trackeo Insights para los últimos titulares.",
    "premium.title": "Planes para entrenadores y federaciones",
    "premium.subtitle": "Desbloquea analíticas, mapas de calor y archivos de video según tu rol.",
    "premium.compare": "Comparar planes",
    "premium.guest_title": "Invitado",
    "premium.guest_price": "Gratis",
    "premium.guest_benefit_1": "Calendario abierto de eventos",
    "premium.guest_benefit_2": "Estadísticas destacadas y noticias",
    "premium.guest_benefit_3": "Localización regional (ES/PT)",
    "premium.premium_title": "Premium",
    "premium.premium_price": "$9 / mes",
    "premium.premium_benefit_1": "Historial completo y analíticas de temporada",
    "premium.premium_benefit_2": "Biblioteca de video con marcadores",
    "premium.premium_benefit_3": "Soporte prioritario en inglés y español",
    "premium.coach_title": "Coach",
    "premium.coach_price": "$29 / mes",
    "premium.coach_benefit_1": "Sincronización de planteles con datos federativos",
    "premium.coach_benefit_2": "Planificación y control de carga",
    "premium.coach_benefit_3": "Invita atletas y gestiona staff",
    "home.federations_title": "Las federaciones cargan de forma segura",
    "home.federations_subtitle": "Socios confiables comparten actuaciones verificadas mediante las APIs de Trackeo.",
    "home.federations_cta": "Enviar resultados oficiales",
    "home.federations_card_1_title": "Canales verificados",
    "home.federations_card_1_body": "Los envíos cifrados con trazabilidad garantizan precisión antes de publicar.",
    "home.federations_card_2_title": "Infraestructura localizada",
    "home.federations_card_2_body": "Nodos edge en São Paulo, Bogotá y Santiago reducen la latencia de carga.",
    "home.federations_card_3_title": "Operaciones en Atlanta",
    "home.federations_card_3_body": "Soporte desde la sede de Trackeo asegura una incorporación fluida.",
    "form.full_name": "Nombre completo",
    "form.full_name_placeholder": "Jane Runner",
    "form.email": "Correo electrónico",
    "form.email_placeholder": "tu@ejemplo.com",
    "form.role": "Rol",
    "form.role_placeholder": "atleta",
    "form.password": "Contraseña",
    "form.password_placeholder": "Password123",
    "form.event_name": "Nombre",
    "form.event_name_placeholder": "Meeting de verano",
    "form.location": "Ubicación",
    "form.location_placeholder": "Lisboa, Portugal",
    "form.start_date": "Fecha de inicio",
    "form.end_date": "Fecha de fin",
    "form.federation_id": "ID de federación",
    "form.federation_id_placeholder": "Opcional",
    "profiles.title": "Perfiles de atletas y staff",
    "profiles.subtitle": "Busca cuentas federadas con historial verificado y biografías multilingües.",
    "profiles.refresh": "Actualizar perfiles",
    "profiles.create": "Crear nuevo perfil",
    "profiles.list_title": "Directorio",
    "profiles.list_subtitle": "Datos en vivo del servicio de cuentas de Trackeo.",
    "profiles.filter_placeholder": "Filtrar por nombre o correo",
    "profiles.filter_aria": "Filtrar perfiles",
    "profiles.empty": "No se encontraron perfiles.",
    "profiles.hint": "Ajusta los filtros o crea una nueva cuenta desde el registro.",
    "events.title": "Calendario de competencias",
    "events.subtitle": "Monitorea meetings oficiales creados por federaciones y socios de Trackeo.",
    "events.create": "Programar evento",
    "events.refresh": "Actualizar",
    "events.list_title": "Meetings próximos y recientes",
    "events.list_subtitle": "Los datos provienen del servicio de eventos y se actualizan al instante.",
    "events.filter_upcoming": "Mostrar solo próximos",
    "events.empty": "Aún no hay eventos publicados.",
    "events.hint": "Crea un meeting o solicita a tu federación que cargue el calendario oficial.",
    "rosters.title": "Planteles federativos",
    "rosters.subtitle": "Controla elegibilidad, divisiones y staff con actualizaciones en vivo del servicio de planteles.",
    "rosters.refresh": "Actualizar planteles",
    "rosters.list_title": "Últimos envíos",
    "rosters.list_subtitle": "Los planteles verificados llegan mediante cargas seguras de federaciones.",
    "rosters.filter_placeholder": "Filtrar por club o país",
    "rosters.filter_aria": "Filtrar planteles",
    "rosters.empty": "Todavía no hay planteles disponibles.",
    "rosters.hint": "Las federaciones pueden cargar un archivo desde la vista segura.",
    "login.title": "Inicia sesión en Trackeo",
    "login.subtitle": "Usa tu correo verificado para acceder a las herramientas premium.",
    "login.submit": "Iniciar sesión",
    "login.switch": "¿Necesitas una cuenta?",
    "login.switch_link": "Créala ahora.",
    "signup.title": "Crea tu cuenta Trackeo",
    "signup.subtitle": "Únete para gestionar planteles, seguir eventos y desbloquear analíticas.",
    "signup.tier": "Nivel de suscripción",
    "signup.tier_free": "Gratis",
    "signup.tier_premium": "Premium",
    "signup.tier_coach": "Coach",
    "signup.tier_federation": "Federación",
    "signup.role_fan": "Fan",
    "signup.role_athlete": "Atleta",
    "signup.role_coach": "Coach",
    "signup.role_federation": "Federación",
    "signup.role_scout": "Scout",
    "signup.submit": "Crear cuenta",
    "signup.switch": "¿Ya estás registrado?",
    "signup.switch_link": "Inicia sesión.",
    "federations.title": "Cargas seguras para federaciones",
    "federations.subtitle": "Envía paquetes cifrados con trazabilidad y verificación automática.",
    "federations.refresh": "Actualizar envíos",
    "federations.form_title": "Subir archivos oficiales",
    "federations.form_subtitle": "Proporciona un enlace firmado. Trackeo valida el checksum y procesa de forma asíncrona.",
    "federations.token": "Token de acceso",
    "federations.token_placeholder": "Token Bearer",
    "federations.name": "Nombre de la federación",
    "federations.name_placeholder": "Confederación Sudamericana",
    "federations.email_placeholder": "contacto@federacion.org",
    "federations.payload": "URL segura del paquete",
    "federations.payload_placeholder": "https://storage.ejemplo.com/resultados.json",
    "federations.notes": "Notas (opcional)",
    "federations.notes_placeholder": "Describe el evento o agrega detalles de validación",
    "federations.submit": "Enviar para procesamiento",
    "federations.submissions_title": "Historial de envíos",
    "federations.submissions_subtitle": "Controla el procesamiento, checksum y verificación.",
    "federations.submissions_empty": "Aún no hay envíos. Carga tu primer archivo oficial para comenzar.",
    "about.title": "Acerca de Trackeo",
    "about.subtitle": "Construido en Atlanta y potenciado por federaciones de Latinoamérica.",
    "about.mission_title": "Misión",
    "about.mission_subtitle": "Potenciamos atletas con datos confiables, cobertura multilingüe y acceso equitativo.",
    "about.mission_body_1": "Trackeo centraliza datos de competencia de 19 federaciones y ofrece insights en inglés, español y portugués.",
    "about.mission_body_2": "Apoyamos a entrenadores con analíticas, acercamos historias a los fans y simplificamos el cumplimiento para el personal federativo.",
    "about.team_title": "Equipo y socios",
    "about.team_subtitle": "Colaboramos con estadísticos, periodistas y federaciones en toda la región.",
    "about.team_item_1_title": "Sede Atlanta",
    "about.team_item_1_body": "Producto, ingeniería y alianzas operan desde Atlanta coordinando cobertura multilingüe.",
    "about.team_item_2_title": "Oficinas regionales",
    "about.team_item_2_body": "Corresponsales en Bogotá, São Paulo, Santiago y Ciudad de México verifican resultados y producen noticias.",
    "about.team_item_3_title": "Consejo federativo",
    "about.team_item_3_body": "Un consejo asesor de líderes federativos garantiza estándares de seguridad y accesibilidad.",
  },
  pt: {
    "badge.beta": "Beta",
    "nav.home": "Início",
    "nav.profiles": "Perfis",
    "nav.events": "Eventos",
    "nav.rosters": "Elencos",
    "nav.federations": "Federações",
    "nav.about": "Sobre",
    "locale.label": "Escolher idioma",
    "action.login": "Entrar",
    "action.signup": "Criar conta",
    "footer.powered": "Trackeo · Impulsionado por FastAPI · Base da API:",
    "footer.location": "Sediada em Atlanta, GA · Expandindo pela América do Sul com parceiros locais.",
    "hero.eyebrow": "Inteligência do atletismo latino-americano",
    "hero.title": "Trackeo conecta federações, técnicos e fãs pelas Américas.",
    "hero.description": "Explore performances verificadas, notícias multilíngues e insights premium que destacam o atletismo de São Paulo a Bogotá. Construído em Atlanta para o continente.",
    "hero.explore": "Explorar como convidado",
    "hero.subscribe": "Ver planos para técnicos",
    "preview.title": "Destaque regional",
    "preview.subtitle": "19 federações transmitindo parciais e heat sheets em tempo real.",
    "preview.metric_meets": "Competições verificadas",
    "preview.metric_athletes": "Atletas monitorados",
    "preview.metric_rosters": "Atualizações de elencos",
    "search.title": "Pesquise o universo Trackeo",
    "search.subtitle": "Encontre atletas, eventos, elencos e notícias bilíngues em um só lugar.",
    "search.placeholder": "Busque por atleta, clube ou meeting",
    "search.aria": "Pesquisar na Trackeo",
    "search.filters": "Categorias de busca",
    "search.filter_all": "Tudo",
    "search.filter_athletes": "Atletas",
    "search.filter_events": "Eventos",
    "search.filter_rosters": "Elencos",
    "search.filter_news": "Notícias",
    "search.empty": "Comece digitando para explorar o universo de dados da Trackeo.",
    "search.no_results": "Nenhum resultado. Ajuste os filtros ou confira a grafia.",
    "home.athletes_title": "Atletas",
    "home.athletes_subtitle": "Navegue pelo elenco ou destaque um talento da sua federação.",
    "home.athletes_seed": "Recarregar atletas de exemplo",
    "home.athletes_form_title": "Criar perfil de atleta",
    "home.athletes_submit": "Registrar atleta",
    "home.athletes_empty": "Nenhum atleta registrado ainda.",
    "home.athletes_hint": "Use o formulário ou carregue atletas de exemplo para preencher o elenco.",
    "home.events_title": "Eventos",
    "home.events_subtitle": "Acompanhe as competições de Atlanta a Buenos Aires.",
    "home.events_seed": "Recarregar eventos de exemplo",
    "home.events_form_title": "Agendar novo meeting",
    "home.events_submit": "Criar evento",
    "home.events_empty": "Nenhum evento agendado ainda.",
    "home.events_hint": "Use o formulário ou recarregue o calendário curado.",
    "home.rosters_title": "Elencos",
    "home.rosters_subtitle": "Mantenha as equipes alinhadas com elegibilidade verificada.",
    "home.rosters_empty": "Nenhum elenco disponível ainda.",
    "home.rosters_hint": "Federações fazem upload direto para publicação imediata.",
    "home.news_title": "Notícias",
    "home.news_subtitle": "Cobertura bilíngue com correspondentes e parceiros Trackeo.",
    "home.news_empty": "Nenhuma notícia publicada ainda.",
    "home.news_hint": "Siga o Trackeo Insights para as últimas manchetes.",
    "premium.title": "Planos para técnicos e federações",
    "premium.subtitle": "Desbloqueie análises, mapas de calor e arquivos de vídeo conforme seu papel.",
    "premium.compare": "Comparar planos",
    "premium.guest_title": "Convidado",
    "premium.guest_price": "Gratuito",
    "premium.guest_benefit_1": "Calendário aberto de eventos",
    "premium.guest_benefit_2": "Estatísticas e notícias em destaque",
    "premium.guest_benefit_3": "Localização regional (ES/PT)",
    "premium.premium_title": "Premium",
    "premium.premium_price": "US$9 / mês",
    "premium.premium_benefit_1": "Histórico completo e análises da temporada",
    "premium.premium_benefit_2": "Biblioteca de vídeos com marcadores",
    "premium.premium_benefit_3": "Suporte prioritário em inglês e espanhol",
    "premium.coach_title": "Coach",
    "premium.coach_price": "US$29 / mês",
    "premium.coach_benefit_1": "Sincronização de elencos com dados da federação",
    "premium.coach_benefit_2": "Planejamento e controle de carga",
    "premium.coach_benefit_3": "Convide atletas e gerencie equipe",
    "home.federations_title": "Federações enviam com segurança",
    "home.federations_subtitle": "Parceiros confiáveis compartilham performances verificadas pelas APIs da Trackeo.",
    "home.federations_cta": "Enviar resultados oficiais",
    "home.federations_card_1_title": "Pipelines verificados",
    "home.federations_card_1_body": "Envios criptografados com trilhas de auditoria garantem precisão antes da publicação.",
    "home.federations_card_2_title": "Infraestrutura local",
    "home.federations_card_2_body": "Nós edge em São Paulo, Bogotá e Santiago reduzem a latência de upload.",
    "home.federations_card_3_title": "Operações Atlanta",
    "home.federations_card_3_body": "Suporte direto da sede Trackeo garante onboarding suave para toda federação.",
    "form.full_name": "Nome completo",
    "form.full_name_placeholder": "Jane Runner",
    "form.email": "E-mail",
    "form.email_placeholder": "voce@exemplo.com",
    "form.role": "Função",
    "form.role_placeholder": "atleta",
    "form.password": "Senha",
    "form.password_placeholder": "Password123",
    "form.event_name": "Nome",
    "form.event_name_placeholder": "Meeting de verão",
    "form.location": "Local",
    "form.location_placeholder": "Lisboa, Portugal",
    "form.start_date": "Data de início",
    "form.end_date": "Data de término",
    "form.federation_id": "ID da federação",
    "form.federation_id_placeholder": "Opcional",
    "profiles.title": "Perfis de atletas e staff",
    "profiles.subtitle": "Pesquise contas federadas com histórico verificado e bios multilíngues.",
    "profiles.refresh": "Atualizar perfis",
    "profiles.create": "Criar novo perfil",
    "profiles.list_title": "Diretório",
    "profiles.list_subtitle": "Dados ao vivo do serviço de contas Trackeo.",
    "profiles.filter_placeholder": "Filtrar por nome ou e-mail",
    "profiles.filter_aria": "Filtrar perfis",
    "profiles.empty": "Nenhum perfil encontrado.",
    "profiles.hint": "Ajuste os filtros ou crie uma nova conta na página de cadastro.",
    "events.title": "Calendário de competições",
    "events.subtitle": "Monitore meetings oficiais de federações e parceiros Trackeo.",
    "events.create": "Agendar evento",
    "events.refresh": "Atualizar",
    "events.list_title": "Meetings futuros e recentes",
    "events.list_subtitle": "Os dados vêm do serviço de eventos e atualizam instantaneamente.",
    "events.filter_upcoming": "Mostrar apenas futuros",
    "events.empty": "Nenhum evento publicado ainda.",
    "events.hint": "Crie um meeting ou peça para sua federação enviar o calendário oficial.",
    "rosters.title": "Elencos federativos",
    "rosters.subtitle": "Acompanhe elegibilidade, divisões e staff com atualizações ao vivo.",
    "rosters.refresh": "Atualizar elencos",
    "rosters.list_title": "Últimos envios",
    "rosters.list_subtitle": "Elencos verificados chegam por uploads seguros das federações.",
    "rosters.filter_placeholder": "Filtrar por clube ou país",
    "rosters.filter_aria": "Filtrar elencos",
    "rosters.empty": "Nenhum elenco disponível ainda.",
    "rosters.hint": "As federações podem enviar um arquivo pela área segura.",
    "login.title": "Faça login no Trackeo",
    "login.subtitle": "Use seu e-mail verificado para acessar as ferramentas premium.",
    "login.submit": "Entrar",
    "login.switch": "Precisa de uma conta?",
    "login.switch_link": "Crie agora.",
    "signup.title": "Crie sua conta Trackeo",
    "signup.subtitle": "Junte-se para gerenciar elencos, acompanhar eventos e obter análises.",
    "signup.tier": "Plano de assinatura",
    "signup.tier_free": "Gratuito",
    "signup.tier_premium": "Premium",
    "signup.tier_coach": "Coach",
    "signup.tier_federation": "Federação",
    "signup.role_fan": "Fã",
    "signup.role_athlete": "Atleta",
    "signup.role_coach": "Coach",
    "signup.role_federation": "Federação",
    "signup.role_scout": "Olheiro",
    "signup.submit": "Criar conta",
    "signup.switch": "Já possui cadastro?",
    "signup.switch_link": "Faça login.",
    "federations.title": "Uploads seguros das federações",
    "federations.subtitle": "Envie pacotes criptografados com trilhas de auditoria e verificação automática.",
    "federations.refresh": "Atualizar envios",
    "federations.form_title": "Enviar arquivos oficiais",
    "federations.form_subtitle": "Forneça um link assinado. A Trackeo valida o checksum e processa de forma assíncrona.",
    "federations.token": "Token de acesso",
    "federations.token_placeholder": "Token Bearer",
    "federations.name": "Nome da federação",
    "federations.name_placeholder": "Confederação Sul-Americana",
    "federations.email_placeholder": "contato@federacao.org",
    "federations.payload": "URL segura do pacote",
    "federations.payload_placeholder": "https://storage.exemplo.com/resultados.json",
    "federations.notes": "Notas (opcional)",
    "federations.notes_placeholder": "Descreva o evento ou inclua detalhes de validação",
    "federations.submit": "Enviar para processamento",
    "federations.submissions_title": "Histórico de envios",
    "federations.submissions_subtitle": "Acompanhe processamento, checksum e verificação.",
    "federations.submissions_empty": "Nenhum envio ainda. Faça upload do primeiro arquivo oficial.",
    "about.title": "Sobre a Trackeo",
    "about.subtitle": "Construída em Atlanta e impulsionada por federações da América Latina.",
    "about.mission_title": "Missão",
    "about.mission_subtitle": "Amplificamos atletas com dados confiáveis, cobertura multilíngue e acesso equitativo.",
    "about.mission_body_1": "A Trackeo centraliza dados de competição de 19 federações e entrega insights em inglês, espanhol e português.",
    "about.mission_body_2": "Apoiamos técnicos com análises, engajamos fãs com histórias e simplificamos a conformidade para equipes federativas.",
    "about.team_title": "Equipe e parceiros",
    "about.team_subtitle": "Colaboramos com estatísticos, jornalistas e federações em toda a região.",
    "about.team_item_1_title": "Sede Atlanta",
    "about.team_item_1_body": "Produto, engenharia e parcerias operam em Atlanta coordenando cobertura multilíngue.",
    "about.team_item_2_title": "Bureaus regionais",
    "about.team_item_2_body": "Correspondentes em Bogotá, São Paulo, Santiago e Cidade do México verificam resultados e produzem notícias.",
    "about.team_item_3_title": "Conselho federativo",
    "about.team_item_3_body": "Um conselho consultivo garante que a Trackeo atenda padrões de segurança e acessibilidade.",
  },
};
function applyLocale(locale) {
  const resolved = translations[locale] ? locale : "en";
  const dictionary = translations[resolved];
  document.documentElement.lang = resolved;
  document
    .querySelectorAll("[data-l10n-key]")
    .forEach((element) => {
      const key = element.dataset.l10nKey;
      const value = dictionary[key];
      if (value === undefined) {
        return;
      }
      element.textContent = value;
    });
  document
    .querySelectorAll("[data-l10n-placeholder]")
    .forEach((element) => {
      const key = element.dataset.l10nPlaceholder;
      const value = dictionary[key];
      if (value === undefined) {
        return;
      }
      element.setAttribute("placeholder", value);
    });
  document
    .querySelectorAll("[data-l10n-aria-label]")
    .forEach((element) => {
      const key = element.dataset.l10nAriaLabel;
      const value = dictionary[key];
      if (value === undefined) {
        return;
      }
      element.setAttribute("aria-label", value);
    });
  if (localeSwitcher) {
    localeSwitcher.value = resolved;
  }
  try {
    localStorage.setItem("trackeo.locale", resolved);
  } catch (error) {
    // ignore storage issues
  }
  return resolved;
}

const storedLocale = (() => {
  try {
    return localStorage.getItem("trackeo.locale");
  } catch (error) {
    return null;
  }
})();
const activeLocale = applyLocale(storedLocale || navigator.language?.slice(0, 2) || "en");

if (localeSwitcher) {
  localeSwitcher.value = activeLocale;
  localeSwitcher.addEventListener("change", (event) => {
    applyLocale(event.target.value);
  });
}

if (headerLoginButton) {
  headerLoginButton.addEventListener("click", () => {
    window.location.href = "/login";
  });
}

if (headerSignupButton) {
  headerSignupButton.addEventListener("click", () => {
    window.location.href = "/signup";
  });
}

const homeFederationButton = document.querySelector("#home-federation-upload");
if (homeFederationButton) {
  homeFederationButton.addEventListener("click", () => {
    window.location.href = "/federations/upload";
  });
}

const heroExploreButton = document.querySelector("#hero-explore");
const heroSubscribeButton = document.querySelector("#hero-subscribe");
const searchSection = document.querySelector("#search");
const premiumSection = document.querySelector("#premium");

if (heroExploreButton && searchSection) {
  heroExploreButton.addEventListener("click", () => {
    searchSection.scrollIntoView({ behavior: "smooth", block: "center" });
    const searchInput = document.querySelector("#global-search");
    if (searchInput) {
      searchInput.focus({ preventScroll: true });
    }
  });
}

if (heroSubscribeButton && premiumSection) {
  heroSubscribeButton.addEventListener("click", () => {
    premiumSection.scrollIntoView({ behavior: "smooth", block: "start" });
  });
}
const sampleAthletes = [
  {
    full_name: "Ramiro Lightfoot",
    email: "ramiro.lightfoot@example.com",
    role: "athlete",
    password: "Shimmering123",
  },
  {
    full_name: "Sofía Delgado",
    email: "sofia.delgado@example.com",
    role: "athlete",
    password: "Sprinter123",
  },
  {
    full_name: "Liam O'Connor",
    email: "liam.oconnor@example.com",
    role: "athlete",
    password: "Hurdles123",
  },
];

const sampleEvents = [
  {
    name: "Aurora Indoor Classic",
    location: "Oslo, Norway",
    start_date: "2024-02-10",
    end_date: "2024-02-12",
    federation_id: null,
  },
  {
    name: "Sunset Coast Invitational",
    location: "Porto, Portugal",
    start_date: "2024-04-22",
    end_date: "2024-04-24",
    federation_id: null,
  },
  {
    name: "Highlands Distance Festival",
    location: "Edinburgh, Scotland",
    start_date: "2024-09-14",
    end_date: "2024-09-15",
    federation_id: null,
  },
];

const sampleRosters = [
  {
    name: "Club Andino Quito",
    country: "Ecuador",
    division: "U20",
    athletes: 18,
    coach: "María Torres",
    updated_at: "2024-08-11T13:45:00Z",
  },
  {
    name: "São Paulo Relays",
    country: "Brazil",
    division: "Senior",
    athletes: 26,
    coach: "Igor Almeida",
    updated_at: "2024-08-09T09:20:00Z",
  },
  {
    name: "Bogotá Altitude Club",
    country: "Colombia",
    division: "U18",
    athletes: 14,
    coach: "Carolina Ríos",
    updated_at: "2024-08-02T18:10:00Z",
  },
];

const sampleNews = [
  {
    title: "Camila Torres sets new 400m South American record",
    region: "Buenos Aires, AR",
    published_at: "2024-08-13T12:00:00Z",
    excerpt: "The 21-year-old from Córdoba clocked 50.82s at the Copa Cono Sur finale.",
  },
  {
    title: "Bogotá Marathon expands elite field for 2025",
    region: "Bogotá, CO",
    published_at: "2024-08-10T08:30:00Z",
    excerpt: "Trackeo partners with local organizers to deliver real-time splits in Spanish and English.",
  },
  {
    title: "Brazilian U20 relay camp launches in São Paulo",
    region: "São Paulo, BR",
    published_at: "2024-08-05T16:15:00Z",
    excerpt: "Coaches gain access to workload dashboards via the Trackeo Coach tier.",
  },
];

const state = {
  athletes: [],
  events: [],
  rosters: sampleRosters.slice(),
  news: sampleNews.slice(),
  federationToken: null,
};

function formatDate(value) {
  if (!value) {
    return "";
  }
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) {
    return value;
  }
  return date.toLocaleDateString(undefined, {
    year: "numeric",
    month: "short",
    day: "numeric",
  });
}

function isFutureDate(value) {
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) {
    return false;
  }
  return date.getTime() >= Date.now() - 86400000;
}
if (pageId === "home") {
  const athleteList = document.querySelector("#athletes-list");
  const athleteEmpty = document.querySelector("#athletes-empty");
  const athleteForm = document.querySelector("#athlete-form");
  const seedAthletesButton = document.querySelector("#seed-athletes");
  const eventList = document.querySelector("#events-list");
  const eventEmpty = document.querySelector("#events-empty");
  const eventForm = document.querySelector("#event-form");
  const seedEventsButton = document.querySelector("#seed-events");
  const rostersList = document.querySelector("#rosters-list");
  const rostersEmpty = document.querySelector("#rosters-empty");
  const newsList = document.querySelector("#news-list");
  const newsEmpty = document.querySelector("#news-empty");
  const searchInput = document.querySelector("#global-search");
  const searchFilters = document.querySelectorAll(".search-filter");
  const searchResults = document.querySelector("#search-results");
  const searchEmpty = document.querySelector("#search-empty");

  let activeSearchFilter = "all";

  function renderAthletes() {
    if (!athleteList || !athleteEmpty) {
      return;
    }
    athleteList.innerHTML = "";
    if (!state.athletes.length) {
      athleteEmpty.hidden = false;
      return;
    }
    athleteEmpty.hidden = true;
    state.athletes.forEach((athlete) => {
      const item = document.createElement("li");
      item.className = "card";
      const created = athlete.created_at ? new Date(athlete.created_at) : new Date();
      item.innerHTML = `
        <div class="card-meta">
          <span class="tag">${athlete.role}</span>
          <span>${athlete.email}</span>
          <span>${formatDate(created)}</span>
        </div>
        <h3>${athlete.full_name}</h3>
      `;
      athleteList.appendChild(item);
    });
  }

  function renderEvents() {
    if (!eventList || !eventEmpty) {
      return;
    }
    eventList.innerHTML = "";
    if (!state.events.length) {
      eventEmpty.hidden = false;
      return;
    }
    eventEmpty.hidden = true;
    state.events.forEach((event) => {
      const item = document.createElement("li");
      item.className = "card";
      const start = event.start_date ? new Date(event.start_date) : null;
      const end = event.end_date ? new Date(event.end_date) : null;
      const dateRange = start && end ? `${formatDate(start)} – ${formatDate(end)}` : "Date TBA";
      item.innerHTML = `
        <h3>${event.name}</h3>
        <div class="card-meta">
          <span class="tag">${event.location}</span>
          <span>${dateRange}</span>
          ${event.federation_id ? `<span>Federation #${event.federation_id}</span>` : ""}
        </div>
      `;
      eventList.appendChild(item);
    });
  }

  function renderRosters() {
    if (!rostersList || !rostersEmpty) {
      return;
    }
    rostersList.innerHTML = "";
    if (!state.rosters.length) {
      rostersEmpty.hidden = false;
      return;
    }
    rostersEmpty.hidden = true;
    state.rosters.forEach((roster) => {
      const updated = roster.updated_at ? formatDate(roster.updated_at) : "";
      const item = document.createElement("li");
      item.className = "card";
      item.innerHTML = `
        <div class="card-meta">
          <span class="tag">${roster.country}</span>
          <span>${roster.division}</span>
          ${updated ? `<span>Updated ${updated}</span>` : ""}
        </div>
        <h3>${roster.name}</h3>
        <p>${roster.athletes} athletes · Coach ${roster.coach}</p>
      `;
      rostersList.appendChild(item);
    });
  }

  function renderNews() {
    if (!newsList || !newsEmpty) {
      return;
    }
    newsList.innerHTML = "";
    if (!state.news.length) {
      newsEmpty.hidden = false;
      return;
    }
    newsEmpty.hidden = true;
    state.news.forEach((article) => {
      const published = article.published_at ? formatDate(article.published_at) : "";
      const item = document.createElement("li");
      item.className = "card";
      item.innerHTML = `
        <div class="card-meta">
          <span class="tag">${article.region}</span>
          ${published ? `<span>${published}</span>` : ""}
        </div>
        <h3>${article.title}</h3>
        <p>${article.excerpt}</p>
      `;
      newsList.appendChild(item);
    });
  }

  function collectSearchResults() {
    const query = searchInput?.value.trim().toLowerCase() ?? "";
    const results = [];
    const includeCategory = (category) => activeSearchFilter === "all" || activeSearchFilter === category;

    if (includeCategory("athletes")) {
      const athletes = (!query ? state.athletes.slice(0, 4) : state.athletes).filter((athlete) => {
        if (!query) return true;
        return (
          athlete.full_name.toLowerCase().includes(query) ||
          (athlete.email && athlete.email.toLowerCase().includes(query))
        );
      });
      athletes.forEach((athlete) => {
        results.push({
          category: "Athletes",
          title: athlete.full_name,
          subtitle: athlete.email,
          detail: athlete.role,
        });
      });
    }

    if (includeCategory("events")) {
      const events = (!query ? state.events.slice(0, 4) : state.events).filter((event) => {
        if (!query) return true;
        return (
          event.name.toLowerCase().includes(query) ||
          (event.location && event.location.toLowerCase().includes(query))
        );
      });
      events.forEach((event) => {
        const start = event.start_date ? new Date(event.start_date) : null;
        const end = event.end_date ? new Date(event.end_date) : null;
        results.push({
          category: "Events",
          title: event.name,
          subtitle: event.location,
          detail: start && end ? `${formatDate(start)} – ${formatDate(end)}` : "Dates TBA",
        });
      });
    }

    if (includeCategory("rosters")) {
      const rosters = (!query ? state.rosters.slice(0, 4) : state.rosters).filter((roster) => {
        if (!query) return true;
        return (
          roster.name.toLowerCase().includes(query) ||
          (roster.country && roster.country.toLowerCase().includes(query)) ||
          (roster.coach && roster.coach.toLowerCase().includes(query))
        );
      });
      rosters.forEach((roster) => {
        results.push({
          category: "Rosters",
          title: roster.name,
          subtitle: `${roster.country} · ${roster.division}`,
          detail: `${roster.athletes} athletes • Coach ${roster.coach}`,
        });
      });
    }

    if (includeCategory("news")) {
      const news = (!query ? state.news.slice(0, 4) : state.news).filter((article) => {
        if (!query) return true;
        return (
          article.title.toLowerCase().includes(query) ||
          (article.region && article.region.toLowerCase().includes(query)) ||
          (article.excerpt && article.excerpt.toLowerCase().includes(query))
        );
      });
      news.forEach((article) => {
        const published = article.published_at ? formatDate(article.published_at) : null;
        results.push({
          category: "News",
          title: article.title,
          subtitle: article.region,
          detail: published || article.excerpt,
          description: article.excerpt,
        });
      });
    }

    return results.slice(0, 12);
  }

  function renderSearchResults() {
    if (!searchResults || !searchEmpty) {
      return;
    }
    const results = collectSearchResults();
    if (!results.length) {
      const dictionary = translations[document.documentElement.lang] || translations.en;
      searchResults.hidden = true;
      searchEmpty.hidden = false;
      searchEmpty.textContent = searchInput?.value.trim()
        ? dictionary["search.no_results"] || translations.en["search.no_results"]
        : dictionary["search.empty"] || translations.en["search.empty"];
      return;
    }

    searchResults.hidden = false;
    searchEmpty.hidden = true;
    searchResults.innerHTML = "";
    results.forEach((result) => {
      const item = document.createElement("li");
      item.className = "search-result";
      item.innerHTML = `
        <div class="search-result-header">
          <span class="tag">${result.category}</span>
          ${result.subtitle ? `<span>${result.subtitle}</span>` : ""}
        </div>
        <h3>${result.title}</h3>
        ${result.description ? `<p>${result.description}</p>` : result.detail ? `<p>${result.detail}</p>` : ""}
      `;
      searchResults.appendChild(item);
    });
  }

  async function loadAthletes() {
    try {
      const data = await request("/accounts/");
      state.athletes = data;
      renderAthletes();
      renderSearchResults();
    } catch (error) {
      const fallback = sampleAthletes.map((athlete, index) => ({
        ...athlete,
        created_at: new Date(Date.now() - index * 86400000).toISOString(),
      }));
      state.athletes = fallback;
      renderAthletes();
      renderSearchResults();
      notify("error", `Live athlete roster unavailable (${error.message}). Showing sample data.`);
      console.error(error);
    }
  }

  async function loadEvents() {
    try {
      const data = await request("/events/");
      state.events = data;
      renderEvents();
      renderSearchResults();
    } catch (error) {
      const fallback = sampleEvents.map((event, index) => ({
        ...event,
        start_date: event.start_date || new Date(Date.now() + index * 604800000).toISOString(),
        end_date: event.end_date || new Date(Date.now() + (index * 604800000) + 86400000).toISOString(),
      }));
      state.events = fallback;
      renderEvents();
      renderSearchResults();
      notify("error", `Live event calendar unavailable (${error.message}). Showing sample data.`);
      console.error(error);
    }
  }

  function renderStaticSections() {
    renderRosters();
    renderNews();
    renderSearchResults();
  }

  renderStaticSections();

  if (athleteForm) {
    athleteForm.addEventListener("submit", async (event) => {
      event.preventDefault();
      const formData = new FormData(athleteForm);
      const payload = Object.fromEntries(formData.entries());
      try {
        await request("/accounts/register", {
          method: "POST",
          body: JSON.stringify(payload),
        });
        athleteForm.reset();
        notify("success", `Athlete "${payload.full_name}" registered successfully.`);
        await loadAthletes();
      } catch (error) {
        if (error.status === 409) {
          notify("error", "This email is already registered.");
        } else {
          notify("error", `Unable to register athlete: ${error.message}`);
        }
        console.error(error);
      }
    });
  }

  if (eventForm) {
    eventForm.addEventListener("submit", async (event) => {
      event.preventDefault();
      const formData = new FormData(eventForm);
      const payload = Object.fromEntries(formData.entries());
      payload.federation_id = payload.federation_id === "" ? null : Number(payload.federation_id);
      try {
        await request("/events/", {
          method: "POST",
          body: JSON.stringify(payload),
        });
        eventForm.reset();
        notify("success", `Event "${payload.name}" created successfully.`);
        await loadEvents();
      } catch (error) {
        notify("error", `Unable to create event: ${error.message}`);
        console.error(error);
      }
    });
  }

  async function seedAthletes() {
    const existingEmails = new Set(state.athletes.map((athlete) => athlete.email));
    for (const athlete of sampleAthletes) {
      if (existingEmails.has(athlete.email)) {
        continue;
      }
      try {
        await request("/accounts/register", {
          method: "POST",
          body: JSON.stringify(athlete),
        });
      } catch (error) {
        if (error.status !== 409) {
          console.warn("Failed to seed athlete", athlete.email, error);
        }
      }
    }
    await loadAthletes();
    notify("success", "Sample athletes are ready.");
  }

  async function seedEvents() {
    const existingNames = new Set(state.events.map((event) => event.name));
    for (const event of sampleEvents) {
      if (existingNames.has(event.name)) {
        continue;
      }
      try {
        await request("/events/", {
          method: "POST",
          body: JSON.stringify(event),
        });
      } catch (error) {
        if (error.status !== 400) {
          console.warn("Failed to seed event", event.name, error);
        }
      }
    }
    await loadEvents();
    notify("success", "Sample events are ready.");
  }

  if (seedAthletesButton) {
    seedAthletesButton.addEventListener("click", async () => {
      seedAthletesButton.disabled = true;
      await seedAthletes();
      seedAthletesButton.disabled = false;
    });
  }

  if (seedEventsButton) {
    seedEventsButton.addEventListener("click", async () => {
      seedEventsButton.disabled = true;
      await seedEvents();
      seedEventsButton.disabled = false;
    });
  }

  if (searchInput) {
    searchInput.addEventListener("input", renderSearchResults);
  }

  searchFilters.forEach((button) => {
    button.addEventListener("click", () => {
      if (button.dataset.filter === activeSearchFilter) {
        return;
      }
      activeSearchFilter = button.dataset.filter;
      searchFilters.forEach((btn) => {
        const isActive = btn === button;
        btn.classList.toggle("active", isActive);
        btn.setAttribute("aria-selected", String(isActive));
        if (isActive) {
          btn.focus();
        }
      });
      renderSearchResults();
    });
  });

  (async () => {
    await loadAthletes();
    if (!state.athletes.length) {
      await seedAthletes();
    }
    await loadEvents();
    if (!state.events.length) {
      await seedEvents();
    }
  })();
}
if (pageId === "profiles") {
  const list = document.querySelector("#profiles-list");
  const empty = document.querySelector("#profiles-empty");
  const filterInput = document.querySelector("#profiles-filter");
  const refreshButton = document.querySelector("#profiles-refresh");
  const createButton = document.querySelector("#profiles-create");

  let profiles = [];

  function renderProfiles() {
    if (!list || !empty) {
      return;
    }
    const query = filterInput?.value.trim().toLowerCase() ?? "";
    const filtered = profiles.filter((profile) => {
      if (!query) return true;
      return (
        profile.full_name.toLowerCase().includes(query) ||
        (profile.email && profile.email.toLowerCase().includes(query))
      );
    });

    list.innerHTML = "";
    if (!filtered.length) {
      empty.hidden = false;
      return;
    }
    empty.hidden = true;
    filtered.forEach((profile) => {
      const item = document.createElement("li");
      item.className = "card";
      const created = formatDate(profile.created_at);
      item.innerHTML = `
        <div class="card-meta">
          <span class="tag">${profile.role}</span>
          <span>${profile.email}</span>
          ${created ? `<span>${created}</span>` : ""}
        </div>
        <h3>${profile.full_name}</h3>
      `;
      list.appendChild(item);
    });
  }

  async function loadProfiles() {
    try {
      profiles = await request("/accounts/");
      renderProfiles();
    } catch (error) {
      profiles = sampleAthletes.map((athlete, index) => ({
        ...athlete,
        id: index + 1,
        created_at: new Date(Date.now() - index * 86400000).toISOString(),
      }));
      renderProfiles();
      notify("error", `Unable to fetch live profiles (${error.message}). Showing sample data.`);
      console.error(error);
    }
  }

  if (filterInput) {
    filterInput.addEventListener("input", renderProfiles);
  }

  if (refreshButton) {
    refreshButton.addEventListener("click", loadProfiles);
  }

  if (createButton) {
    createButton.addEventListener("click", () => {
      window.location.href = "/signup";
    });
  }

  loadProfiles();
}
if (pageId === "events") {
  const list = document.querySelector("#events-page-list");
  const empty = document.querySelector("#events-page-empty");
  const refreshButton = document.querySelector("#events-refresh");
  const createButton = document.querySelector("#events-create");
  const upcomingToggle = document.querySelector("#events-only-upcoming");

  let events = [];

  function renderEventsPage() {
    if (!list || !empty) {
      return;
    }
    const onlyUpcoming = upcomingToggle?.checked ?? false;
    const items = events
      .slice()
      .filter((event) => (onlyUpcoming ? isFutureDate(event.start_date || event.created_at) : true))
      .sort((a, b) => {
        const aDate = new Date(a.start_date || a.created_at || 0).getTime();
        const bDate = new Date(b.start_date || b.created_at || 0).getTime();
        return bDate - aDate;
      });

    list.innerHTML = "";
    if (!items.length) {
      empty.hidden = false;
      return;
    }
    empty.hidden = true;
    items.forEach((event) => {
      const start = event.start_date ? formatDate(event.start_date) : "";
      const end = event.end_date ? formatDate(event.end_date) : "";
      const item = document.createElement("li");
      item.className = "card";
      item.innerHTML = `
        <div class="card-meta">
          <span class="tag">${event.location || "TBA"}</span>
          ${start ? `<span>${start}${end ? ` – ${end}` : ""}</span>` : ""}
          ${event.federation_id ? `<span>Federation #${event.federation_id}</span>` : ""}
        </div>
        <h3>${event.name}</h3>
      `;
      list.appendChild(item);
    });
  }

  async function loadEventsPage() {
    try {
      events = await request("/events/");
      renderEventsPage();
    } catch (error) {
      events = sampleEvents.map((event, index) => ({
        ...event,
        start_date: event.start_date || new Date(Date.now() + index * 604800000).toISOString(),
        end_date: event.end_date || new Date(Date.now() + (index * 604800000) + 86400000).toISOString(),
      }));
      renderEventsPage();
      notify("error", `Unable to load events (${error.message}). Showing sample data.`);
      console.error(error);
    }
  }

  if (refreshButton) {
    refreshButton.addEventListener("click", loadEventsPage);
  }

  if (createButton) {
    createButton.addEventListener("click", () => {
      window.location.href = "/#events";
    });
  }

  if (upcomingToggle) {
    upcomingToggle.addEventListener("change", renderEventsPage);
  }

  loadEventsPage();
}
if (pageId === "rosters") {
  const list = document.querySelector("#rosters-page-list");
  const empty = document.querySelector("#rosters-page-empty");
  const refreshButton = document.querySelector("#rosters-refresh");
  const filterInput = document.querySelector("#rosters-filter");

  let rosters = [];

  function renderRostersPage() {
    if (!list || !empty) {
      return;
    }
    const query = filterInput?.value.trim().toLowerCase() ?? "";
    const filtered = rosters.filter((roster) => {
      if (!query) return true;
      return (
        roster.name.toLowerCase().includes(query) ||
        (roster.country && roster.country.toLowerCase().includes(query)) ||
        (roster.coach && roster.coach.toLowerCase().includes(query))
      );
    });

    list.innerHTML = "";
    if (!filtered.length) {
      empty.hidden = false;
      return;
    }
    empty.hidden = true;
    filtered.forEach((roster) => {
      const updated = roster.updated_at ? formatDate(roster.updated_at) : "";
      const item = document.createElement("li");
      item.className = "card";
      item.innerHTML = `
        <div class="card-meta">
          <span class="tag">${roster.country}</span>
          <span>${roster.division || ""}</span>
          ${updated ? `<span>${updated}</span>` : ""}
        </div>
        <h3>${roster.name}</h3>
        <p>${roster.athletes ?? "--"} athletes · Coach ${roster.coach || "TBA"}</p>
      `;
      list.appendChild(item);
    });
  }

  async function loadRostersPage() {
    try {
      rosters = await request("/rosters/");
      renderRostersPage();
    } catch (error) {
      rosters = sampleRosters.map((roster) => ({
        ...roster,
        updated_at: roster.updated_at || new Date().toISOString(),
      }));
      renderRostersPage();
      notify("error", `Unable to load rosters (${error.message}). Showing sample data.`);
      console.error(error);
    }
  }

  if (filterInput) {
    filterInput.addEventListener("input", renderRostersPage);
  }

  if (refreshButton) {
    refreshButton.addEventListener("click", loadRostersPage);
  }

  loadRostersPage();
}
const TOKEN_STORAGE_KEY = "trackeo.auth.token";
const TOKEN_EXPIRY_KEY = "trackeo.auth.expires";
const TOKEN_TIER_KEY = "trackeo.auth.tier";

function storeAuthToken(token, expiresAt, tier) {
  try {
    if (token) {
      localStorage.setItem(TOKEN_STORAGE_KEY, token);
    }
    if (expiresAt) {
      const value = expiresAt instanceof Date ? expiresAt.toISOString() : String(expiresAt);
      localStorage.setItem(TOKEN_EXPIRY_KEY, value);
    }
    if (tier) {
      localStorage.setItem(TOKEN_TIER_KEY, tier);
    }
  } catch (error) {
    console.warn("Unable to persist auth token", error);
  }
}

function readAuthToken() {
  try {
    const token = localStorage.getItem(TOKEN_STORAGE_KEY);
    const expires = localStorage.getItem(TOKEN_EXPIRY_KEY);
    return {
      token,
      expiresAt: expires,
      tier: localStorage.getItem(TOKEN_TIER_KEY),
    };
  } catch (error) {
    return { token: null, expiresAt: null, tier: null };
  }
}
if (pageId === "login") {
  const form = document.querySelector("#login-form");

  if (form) {
    form.addEventListener("submit", async (event) => {
      event.preventDefault();
      const formData = new FormData(form);
      const params = new URLSearchParams();
      formData.forEach((value, key) => {
        params.append(key, value);
      });
      try {
        const response = await fetch(`${API_BASE}/accounts/login`, {
          method: "POST",
          headers: {
            "Content-Type": "application/x-www-form-urlencoded",
          },
          body: params.toString(),
        });
        if (!response.ok) {
          throw new Error("Incorrect credentials");
        }
        const data = await response.json();
        storeAuthToken(data.access_token, data.expires_at, data.subscription_tier);
        state.federationToken = data.access_token;
        notify("success", "Signed in successfully. Token stored for secure uploads.");
        window.location.href = "/";
      } catch (error) {
        notify("error", error.message || "Unable to sign in.");
        console.error(error);
      }
    });
  }
}
if (pageId === "signup") {
  const form = document.querySelector("#signup-form");

  if (form) {
    form.addEventListener("submit", async (event) => {
      event.preventDefault();
      const formData = new FormData(form);
      const payload = Object.fromEntries(formData.entries());
      try {
        await request("/accounts/register", {
          method: "POST",
          body: JSON.stringify(payload),
        });
        notify("success", "Account created successfully. Sign in to continue.");
        window.location.href = "/login";
      } catch (error) {
        if (error.status === 409) {
          notify("error", "This email is already registered.");
        } else {
          notify("error", `Unable to create account: ${error.message}`);
        }
        console.error(error);
      }
    });
  }
}
if (pageId === "federations-upload") {
  const form = document.querySelector("#federations-upload-form");
  const refreshButton = document.querySelector("#federations-refresh");
  const list = document.querySelector("#federations-submissions");
  const empty = document.querySelector("#federations-submissions-empty");

  function normalizeToken(value) {
    if (!value) {
      return null;
    }
    return value.startsWith("Bearer ") ? value : `Bearer ${value}`;
  }

  function renderSubmissions(submissions) {
    if (!list || !empty) {
      return;
    }
    list.innerHTML = "";
    if (!submissions.length) {
      empty.hidden = false;
      return;
    }
    empty.hidden = true;
    submissions
      .slice()
      .sort((a, b) => new Date(b.submitted_at).getTime() - new Date(a.submitted_at).getTime())
      .forEach((submission) => {
        const submitted = formatDate(submission.submitted_at);
        const processed = submission.verified_at ? formatDate(submission.verified_at) : null;
        const item = document.createElement("li");
        item.className = "card";
        item.innerHTML = `
          <div class="card-meta">
            <span class="tag">${submission.federation_name}</span>
            <span>${submission.status}</span>
            ${submitted ? `<span>${submitted}</span>` : ""}
          </div>
          <h3>${submission.payload_url}</h3>
          <p>${submission.notes || ""}</p>
          ${processed ? `<p>Verified ${processed}</p>` : ""}
        `;
        list.appendChild(item);
      });
  }

  async function loadSubmissions(token) {
    const authHeader = token || normalizeToken(state.federationToken) || normalizeToken(readAuthToken().token);
    if (!authHeader) {
      notify("error", "Provide an access token to view submissions.");
      return;
    }
    state.federationToken = authHeader;
    try {
      const submissions = await request("/federations/submissions", {
        headers: {
          Authorization: authHeader,
        },
      });
      renderSubmissions(submissions);
    } catch (error) {
      if (error.status === 401 || error.status === 403) {
        notify("error", "Token is invalid or lacks required permissions.");
      } else {
        notify("error", `Unable to load submissions: ${error.message}`);
      }
      console.error(error);
    }
  }

  if (form) {
    form.addEventListener("submit", async (event) => {
      event.preventDefault();
      const formData = new FormData(form);
      const tokenInput = formData.get("token");
      const authHeader = normalizeToken(tokenInput || readAuthToken().token);
      if (!authHeader) {
        notify("error", "A bearer token is required to submit files.");
        return;
      }
      state.federationToken = authHeader;
      if (tokenInput) {
        const rawToken = tokenInput.toString().replace(/^Bearer\s+/i, "");
        storeAuthToken(rawToken, new Date(Date.now() + 3600_000).toISOString(), readAuthToken().tier);
      }
      const payload = Object.fromEntries(formData.entries());
      delete payload.token;
      try {
        await request("/federations/submissions", {
          method: "POST",
          headers: {
            Authorization: authHeader,
          },
          body: JSON.stringify(payload),
        });
        form.reset();
        notify("success", "Submission queued for processing.");
        await loadSubmissions(authHeader);
      } catch (error) {
        notify("error", `Upload failed: ${error.message}`);
        console.error(error);
      }
    });
  }

  if (refreshButton) {
    refreshButton.addEventListener("click", () => {
      loadSubmissions();
    });
  }

  const stored = readAuthToken();
  if (stored.token) {
    state.federationToken = normalizeToken(stored.token);
    loadSubmissions(state.federationToken);
  }
}
