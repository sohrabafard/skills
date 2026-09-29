export class MemoryStore {
    durable = false;
    data = new Map();
    async get(key) {
        return this.data.get(key);
    }
    async set(key, value) {
        this.data.set(key, value);
    }
    async delete(key) {
        this.data.delete(key);
    }
    async clear() {
        this.data.clear();
    }
    async deleteByAccount(accountKey) {
        let removed = 0;
        for (const [key, value] of this.data){
            if (value.accountKey === accountKey) {
                this.data.delete(key);
                removed += 1;
            }
        }
        return removed;
    }
}
