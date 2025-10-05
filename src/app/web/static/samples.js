export const sampleAthletes = [
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

export const sampleEvents = [
  {
    id: 1,
    name: "Aurora Indoor Classic",
    location: "Oslo, Norway",
    start_date: "2024-02-10",
    end_date: "2024-02-12",
    federation_id: null,
  },
  {
    id: 2,
    name: "Sunset Coast Invitational",
    location: "Porto, Portugal",
    start_date: "2024-04-22",
    end_date: "2024-04-24",
    federation_id: null,
  },
  {
    id: 3,
    name: "Highlands Distance Festival",
    location: "Edinburgh, Scotland",
    start_date: "2024-09-14",
    end_date: "2024-09-15",
    federation_id: null,
  },
];

export const sampleFederations = [
  {
    id: 1,
    name: "Confederação Brasileira de Atletismo",
    country: "Brazil",
    clubs: 146,
  },
  {
    id: 2,
    name: "Federación Colombiana de Atletismo",
    country: "Colombia",
    clubs: 78,
  },
  {
    id: 3,
    name: "Federación Atlética de Chile",
    country: "Chile",
    clubs: 52,
  },
];

export const sampleResults = [
  {
    event: "Campeonato Sudamericano U23",
    discipline: "100m Final",
    medalists: [
      "🥇 Camila Torres (ARG) – 11.28",
      "🥈 Mariana Costa (BRA) – 11.35",
      "🥉 Isabela Queiroz (BRA) – 11.41",
    ],
  },
  {
    event: "Relays de São Paulo",
    discipline: "4x400m Mixed",
    medalists: [
      "🥇 São Paulo Relays – 3:18.44",
      "🥈 Bogotá Altitude Club – 3:20.02",
      "🥉 Club Andino Quito – 3:21.88",
    ],
  },
  {
    event: "Gran Premio Ciudad de México",
    discipline: "Long Jump Final",
    medalists: [
      "🥇 Thiago López (BRA) – 8.08m",
      "🥈 Javier Méndez (MEX) – 7.95m",
      "🥉 Mateo Herrera (COL) – 7.88m",
    ],
  },
];

export const sampleRosters = [
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

export const sampleNews = [
  {
    title: "Camila Torres sets new 400m South American record",
    region: "Buenos Aires, AR",
    published_at: "2024-08-13T12:00:00Z",
    excerpt:
      "The 21-year-old from Córdoba clocked 50.82s at the Copa Cono Sur finale.",
  },
  {
    title: "Bogotá Marathon expands elite field for 2025",
    region: "Bogotá, CO",
    published_at: "2024-08-10T08:30:00Z",
    excerpt:
      "Trackeo partners with local organizers to deliver real-time splits in Spanish and English.",
  },
  {
    title: "Brazilian U20 relay camp launches in São Paulo",
    region: "São Paulo, BR",
    published_at: "2024-08-05T16:15:00Z",
    excerpt:
      "Coaches gain access to workload dashboards via the Trackeo Coach tier.",
  },
];

export function buildSampleEventDetail(eventId = 1) {
  const now = new Date();
  const start = new Date(now.getTime() - 3600000);
  const end = new Date(now.getTime() + 2 * 86400000);
  const sessionOneStart = new Date(now.getTime() - 1800000);
  const sessionOneEnd = new Date(now.getTime() + 3600000);
  const sessionTwoStart = new Date(now.getTime() + 7200000);
  const sessionTwoEnd = new Date(now.getTime() + 10800000);
  const sessions = [
    {
      id: 1,
      event_id: eventId,
      name: "Morning Session",
      start_time: sessionOneStart.toISOString(),
      end_time: sessionOneEnd.toISOString(),
      venue: "Main Stadium",
      status: "live",
      description: "Sample data session",
    },
    {
      id: 2,
      event_id: eventId,
      name: "Evening Finals",
      start_time: sessionTwoStart.toISOString(),
      end_time: sessionTwoEnd.toISOString(),
      venue: "Main Stadium",
      status: "scheduled",
      description: "Sample finals block",
    },
  ];
  const disciplines = [
    {
      id: 1,
      event_id: eventId,
      session_id: sessions[0].id,
      name: "100m",
      category: "Sprints",
      round_name: "Final",
      scheduled_start: sessionOneStart.toISOString(),
      scheduled_end: new Date(sessionOneStart.getTime() + 1800000).toISOString(),
      status: "finalized",
      venue: "Main Stadium",
      order: 1,
      session: { ...sessions[0] },
      entries: [
        {
          id: 1,
          discipline_id: 1,
          athlete_name: "Valentina Ríos",
          team_name: "Andean Flyers",
          status: "finished",
          lane: "4",
          position: 1,
          result: "11.32s",
          points: 12,
          updated_at: now.toISOString(),
        },
        {
          id: 2,
          discipline_id: 1,
          athlete_name: "Mateo Herrera",
          team_name: "Caribbean Storm",
          status: "finished",
          lane: "5",
          position: 2,
          result: "11.40s",
          points: 10,
          updated_at: now.toISOString(),
        },
        {
          id: 3,
          discipline_id: 1,
          athlete_name: "Camila Ibáñez",
          team_name: "Patagonia Peaks",
          status: "finished",
          lane: "3",
          position: 3,
          result: "11.55s",
          points: 8,
          updated_at: now.toISOString(),
        },
        {
          id: 4,
          discipline_id: 1,
          athlete_name: "Thiago López",
          team_name: "Amazon Striders",
          status: "finished",
          lane: "2",
          position: 4,
          result: "11.60s",
          points: 6,
          updated_at: now.toISOString(),
        },
      ],
    },
    {
      id: 2,
      event_id: eventId,
      session_id: sessions[0].id,
      name: "Long Jump",
      category: "Jumps",
      round_name: "Final",
      scheduled_start: new Date(sessionOneStart.getTime() + 2400000).toISOString(),
      scheduled_end: new Date(sessionOneStart.getTime() + 5400000).toISOString(),
      status: "live",
      venue: "Jumps Apron",
      order: 2,
      session: { ...sessions[0] },
      entries: [
        {
          id: 5,
          discipline_id: 2,
          athlete_name: "Renata Gómez",
          team_name: "Cusco Distance",
          status: "live",
          lane: null,
          position: null,
          result: "6.48m",
          points: null,
          updated_at: now.toISOString(),
        },
        {
          id: 6,
          discipline_id: 2,
          athlete_name: "Daniel Torres",
          team_name: "Granada Hurdlers",
          status: "live",
          lane: null,
          position: null,
          result: "6.30m",
          points: null,
          updated_at: now.toISOString(),
        },
      ],
    },
    {
      id: 3,
      event_id: eventId,
      session_id: sessions[1].id,
      name: "4x400m Relay",
      category: "Relays",
      round_name: "Final",
      scheduled_start: sessionTwoStart.toISOString(),
      scheduled_end: new Date(sessionTwoStart.getTime() + 3600000).toISOString(),
      status: "scheduled",
      venue: "Main Stadium",
      order: 1,
      session: { ...sessions[1] },
      entries: [
        {
          id: 7,
          discipline_id: 3,
          athlete_name: "Pacífico Runners",
          team_name: "Pacífico Runners",
          status: "scheduled",
          lane: "4",
          position: null,
          result: null,
          points: null,
          updated_at: now.toISOString(),
        },
        {
          id: 8,
          discipline_id: 3,
          athlete_name: "Quito Relays",
          team_name: "Quito Relays",
          status: "scheduled",
          lane: "5",
          position: null,
          result: null,
          points: null,
          updated_at: now.toISOString(),
        },
      ],
    },
  ];

  return {
    id: eventId,
    name: "Aurora Indoor Classic",
    location: "Oslo, Norway",
    start_date: start.toISOString(),
    end_date: end.toISOString(),
    federation_id: null,
    sessions,
    disciplines,
    latest_update: now.toISOString(),
  };
}
