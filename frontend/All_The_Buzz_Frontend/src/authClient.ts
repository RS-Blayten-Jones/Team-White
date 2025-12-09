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

export async function exchangeTokenForCredentials(token: string) {
  const res = await axios.post('http://localhost:8080/auth/verify', { token }, {
    headers: { 'Content-Type': 'application/json',
      'Bearer': token
     }
  })
  console.log("response data back from our server.py route straight to his auth server: ", res.data)
  return res.data
}





