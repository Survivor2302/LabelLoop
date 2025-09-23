import { createApi, fetchBaseQuery } from '@reduxjs/toolkit/query/react';

export type ComponentHealth = {
  status: 'ok' | 'error';
  message?: string | null;
  latency_ms?: number | null;
};

export type Health = {
  status: 'ok' | 'degraded';
  components: Record<string, ComponentHealth>;
};

export type DBHealth = ComponentHealth;

export const healthApi = createApi({
  reducerPath: 'healthApi',
  baseQuery: fetchBaseQuery({
    baseUrl: `${process.env.NEXT_PUBLIC_API_URL}/health`,
    prepareHeaders: async headers => {
      return headers;
    },
  }),
  tagTypes: ['Health'],
  endpoints: builder => ({
    health: builder.query<Health, void>({
      query() {
        return {
          url: `/`,
          method: 'GET',
        };
      },
      providesTags: ['Health'],
    }),
  }),
});

export const { useHealthQuery } = healthApi;
