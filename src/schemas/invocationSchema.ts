export interface EpistemicProof {
  proofId: string;
  subClassification: 'empirical' | 'deductive' | 'dialectical' | 'paraconsistent';
  confidence: number;
  timestamp: string;
}

export type RhetoricalPressureTier =
  | 'Discover'
  | 'Secret'
  | 'Transform'
  | 'Instant'
  | 'Master'
  | 'Proven'
  | 'Guaranteed'
  | 'Exclusive'
  | 'Effortless'
  | 'Ultimate';

export interface Invocation {
  id: string;
  title: string;
  tier: RhetoricalPressureTier;
  proof?: EpistemicProof;
  tags: string[];
}
