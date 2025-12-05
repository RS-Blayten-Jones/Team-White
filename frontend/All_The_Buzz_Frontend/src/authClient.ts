import axios from 'axios'


export interface Credentials {
  fName: string
  lName: string
  role: 'Manager' | 'Employee'
  id?: number
  title?: string
  department?: string
  // add other fields if your server returns them
}


export type AuthResponse =
  | Credentials
  | { code: 'InvalidToken' | 'ConfigLoadError' | 
    'ServerConnectionError' | 'AuthServerError' | 
    'UnauthorizedToken'
  }

export async function exchangeTokenForCredentials(authUri: string, token: string): Promise<AuthResponse> {
  const headers = { 'Content-Type': 'application/json' }
  const payload = { token } // NOTE: matches your Python signature: {'token': '<string>'}

  const res = await axios.post(authUri, payload, { headers })
  return res.data as AuthResponse
}





