const getState = ({ getStore, getActions, setStore }) => {
	return {
		store: {
			message: null,
			demo: [
				{
					title: "FIRST",
					background: "white",
					initial: "white"
				},
				{
					title: "SECOND",
					background: "white",
					initial: "white"
				}
			]
		},
		actions: {
			getBooks: async () => {
				try {
					const resp = await fetch(process.env.BACKEND_URL + "/api/books");
					if (!resp.ok) throw new Error('Error registering')
					const data = await resp.json()
					setStore({books: data.books})
				} catch (error) {
					console.log(error);

				}
			},
			logout: ()=>{
				localStorage.removeItem('token');
				setStore({auth: false, user: null, token: null})
			},
			getUserInfo: async() => {
				try {
					const resp = await fetch(process.env.BACKEND_URL + "/api/get_user_info", {
						method: 'GET',
						headers: {
							'Content-Type': 'application/json',
							'Authorization': `Bearer ${localStorage.getItem('token')}`
						},
						
					});
					if (!resp.ok) throw new Error('Error registering')
					const data = await resp.json()
					setStore({token: localStorage.getItem('token'), user: data.user, auth: true})
				} catch (error) {
					console.log(error);

				}
			},
			register: async (formData) => {
				try {
					const resp = await fetch(process.env.BACKEND_URL + "/api/user/register", {
						method: 'POST',
						headers: {
							'Content-Type': 'application/json'
						},
						body: JSON.stringify(formData)
					});
					if (!resp.ok) throw new Error('Error registering')
					const data = await resp.json()
					console.log(data)
				} catch (error) {
					console.log(error);

				}
			},
			login: async (formData) => {
				try {
					const resp = await fetch(process.env.BACKEND_URL + "/api/user/login", {
						method: 'POST',
						headers: {
							'Content-Type': 'application/json'
						},
						body: JSON.stringify(formData)
					});
					if (!resp.ok) throw new Error('Error login in')
					const data = await resp.json()
					setStore({token: data.token, user: data.user, auth: true})
					localStorage.setItem('token', data.token)
				} catch (error) {
					console.log(error);
				}
			},
			// Use getActions to call a function within a fuction
			exampleFunction: () => {
				getActions().changeColor(0, "green");
			},

			getMessage: async () => {
				try {
					// fetching data from the backend
					const resp = await fetch(process.env.BACKEND_URL + "/api/hello")
					const data = await resp.json()
					setStore({ message: data.message })
					// don't forget to return something, that is how the async resolves
					return data;
				} catch (error) {
					console.log("Error loading message from backend", error)
				}
			},
			changeColor: (index, color) => {
				//get the store
				const store = getStore();

				//we have to loop the entire demo array to look for the respective index
				//and change its color
				const demo = store.demo.map((elm, i) => {
					if (i === index) elm.background = color;
					return elm;
				});

				//reset the global store
				setStore({ demo: demo });
			}
		}
	};
};

export default getState;
