const check_info=document.getElementById('find')
    check_info.addEventListener('click',()=>{
        const div_info=document.getElementById('new_creat')
        div_info.innerHTML=""
        const serch_info=document.createElement('input')
        serch_info.type="text"
        const submit_button=document.createElement('button')
        submit_button.type='submit'
        submit_button.textContent="查找"
        div_info.appendChild(serch_info)
        div_info.appendChild(submit_button)

        submit_button.addEventListener('click',async (event)=>{
            event.preventDefault();
        loadIds().then(()=>{
            const text_info=Number(serch_info.value)
            if(ids.includes(text_info))
            {
            
            }
            else{
                alert("未找到id为"+text_info+"的数据")
            }
        })

        })

    })我想让他将查找的id给后端然后后端将完整的一条数据给他，他展现出来