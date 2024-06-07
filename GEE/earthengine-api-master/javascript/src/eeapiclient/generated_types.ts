// TODO(b/70239858): force load module only used in types. Drop when
// goog.requireType is around.
import './domain_object';
import './multipart_request';

import {Serializable, SerializableCtor} from './domain_object';
import {MultipartRequest} from './multipart_request';

/**
 * Used to signal that an argument can be an instance of an interface generated
 * in interface-only mode.
 *
 * Because of structural typing this has no real effect, but it hopefully
 * clarifies method signatures.
 *
 * TODO(b/31583417): Figure out ways to enforce stronger typing.
 */
export interface GeneratedInterface {}

export interface GeneratedRequestParams {
  path: string;
  httpMethod: string;
  /** The id of the called method, from discovery. */
  methodId?: string;
  queryParams?: {
    [key: string]: number|number[]|string|string[]|boolean|boolean[]|undefined
  };
  body?: Serializable|GeneratedInterface|MultipartRequest|null;
  responseCtor?: SerializableCtor<Serializable>;
  /**
   * Whether the end-point is a streaming end-point and its type e.g.
   * 'SERVER_SIDE'.
   */
  streamingType?: string;
}

export interface ApiClientObjectMap<T> { [key: string]: T; }
